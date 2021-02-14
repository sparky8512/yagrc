# Yet Another gRPC Reflection Client

A minimalist [gRPC](https://grpc.io/) reflection client for Python. Reflected grpc type classes can be used either by getting them by the names defined in their proto files, or by importing the same modules you would when using protoc to [generate them](https://grpc.io/docs/languages/python/generated-code/).

Because sometimes, having to run protoc can be inconvenient.

## Prerequisites

To make use of the modules in this project, you will need to be using gRPC services on a server that has  [server reflection](https://github.com/grpc/grpc/blob/master/doc/server-reflection.md) enabled.

## Installation

```shell script
pip install yagrc
```

## Usage

Given the following non-reflection-based client request:
```python
import grpc

from arithmetic import subtract_pb2
from arithmetic import subtract_pb2_grpc

...

with grpc.insecure_channel(target) as channel:
    stub = subtract_pb2_grpc.SubtractionStub(channel)
    response = stub.SubtractOne(subtract_pb2.Minuend(number=5))
```

the equivalent using `yagrc.reflector` would be:
```python
import grpc
from yagrc import reflector as yagrc_reflector

...

reflector = yagrc_reflector.GrpcReflectionClient()

with grpc.insecure_channel(target) as channel:
    reflector.load_protocols(channel, symbols=["Arithmetic.Subtraction"])
    stub_class = reflector.service_stub_class("Arithmetic.Subtraction")
    request_class = reflector.message_class("Arithmetic.Minuend")

    stub = stub_class(channel)
    response = stub.SubtractOne(request_class(number=5))
```

and the equivalent using `yagrc.importer` would be:
```python
import grpc
from yagrc import importer as yagrc_importer

...

importer = yagrc_importer.GrpcImporter()

with grpc.insecure_channel(target) as channel:
    importer.configure(channel, filenames=["arithmetic/subtract.proto"])

    from arithmetic import subtract_pb2
    from arithmetic import subtract_pb2_grpc

    stub = subtract_pb2_grpc.SubtractionStub(channel)
    response = stub.SubtractOne(subtract_pb2.Minuend(number=5))
```

In both cases, the relevant protocol files must first be loaded, using `GrpcReflectionClient.load_protocols` or `GrpcImporter.configure`. The requested files will be loaded in addition to all dependencies of those files. In general, when using the reflector module, requesting to load the file that defines the service you're using will also load any message types used in that service. When using the importer module, it's best to request the proto files corresponding with the `_pb2` modules you import. Or you can just call `GrpcReflectionClient.load_protocols` or `GrpcImporter.configure` without specifying filenames or symbols and files defining all services advertised via reflection will be loaded. See the module documentation for specific detail.

There is also a lazy importer in `yagrc.importer`, which is simpler to use but less flexible:
```python
import grpc
from yagrc import importer as yagrc_importer

yagrc_importer.add_lazy_packages(["arithmetic"])

from arithmetic import subtract_pb2
from arithmetic import subtract_pb2_grpc

...

with grpc.insecure_channel(target) as channel:
    yagrc_importer.resolve_lazy_imports(channel)

    stub = subtract_pb2_grpc.SubtractionStub(channel)
    response = stub.SubtractOne(subtract_pb2.Minuend(number=5))
```

### Practical use of the importer module

The primary motivation for `yagrc.importer` is to provide a drop-in replacement of the protoc-generated modules without having to rewrite the client code to access the classes differently. However, a grpc `channel` is needed to in order to load the protocol files, and that's usually not something you'll want to be opening at the top level of a module, so unless you use the lazy variant, the imports will probably need to be deferred to a function call. You can do this just prior to using the grpc calls, as in the example above, but doing so would result in a lot of unnecessary work every time each function that uses grpc is called.

An alternative is to load them in one place along with the deferred imports and keep track of whether or not it needs to be run:
```python
import grpc

try:
    from arithmetic import subtract_pb2
    from arithmetic import subtract_pb2_grpc
    import_ok = True
except ImportError:
    from yagrc import importer as yagrc_importer
    import_ok = False

def import_protocols(channel):
    importer = yagrc_importer.GrpcImporter()
    importer.configure(channel, filenames=["arithmetic/subtract.proto"])

    global subtract_pb2
    global subtract_pb2_grpc
    from arithmetic import subtract_pb2
    from arithmetic import subtract_pb2_grpc

    global import_ok
    import_ok = True

...

def some_function_that_uses_grpc():
    with grpc.insecure_channel(target) as channel:
        if not import_ok:
            import_protocols(channel)
        stub = subtract_pb2_grpc.SubtractionStub(channel)
        response = stub.SubtractOne(subtract_pb2.Minuend(number=5))
```
With this pattern, if the protoc-generated files are available in the module import path, they will be used. If not, they will be loaded when needed via reflection.

Note that `GrpcImporter.configure` is not especially tread safe, so calling it in multiple threads simultaneously should be avoided. If there is a possibility that multiple threads may run grpc calls simultaneously, it would probably be better to just ensure `GrpcImporter.configure` is called in a main thread prior to starting the other threads.

This is somewhat messy. The lazy import mechanism attempts to cut back on the mess by allowing the imports to happen in advance, outside of function context. The lazy importer example in the prior section will still prefer the protoc-generated files if they are available in the module import path. `importer.resolve_lazy_imports` is safe to call multiple times even if no more imports need to be resolved, it just won't do anything in that case.

## Limitations

For the `_pb2_grpc` modules, the `importer` module only provides the client stub class. It does not provide the client class that uses the `grpc.experimental` API, nor does it provide either of the two server classes. It would be possible to provide these, but the use case for the server classes would be limited to a service implemented on a server that wants to get the protocol modules via reflection from another server that implements the same service, which seems a bit of a stretch. And the experimental API is... well... experimental, which implies its API is subject to change.

## Security considerations

All the functionality that communicates with the grpc reflection service uses a grpc `Channel` passed in by the caller. The security of that communication is only going to be as secure as the channel passed in. However, even if the channel is secure, using classes that are dynamically created based on reflection data is always going to be less secure than using classes that were generated in advance using protoc. Thus, use of the modules in this project is not advised for security sensitive applications.

## Similar projects

[grpc requests](https://github.com/spaceone-dev/grpc_requests) is a Python grpc client that supports reflection, but it exposes a different type class interface than the protoc-generated ones (as far as I can tell...).

[Eagr](https://github.com/kensho-technologies/eagr) includes a Python grpc reflection client interface, but it's a small part of a much larger project, most of which is unrelated to reflection.

There's lots of reflection clients for other languages, too, and probably others for Python. [gRPCurl](https://github.com/fullstorydev/grpcurl), in particular, is useful if you want to examine reflected service protocols interactively.
