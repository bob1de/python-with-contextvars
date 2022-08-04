with-contextvars
================

This module provides ``Set``, a context manager which sets one or more ``contextvars``
variables upon activation and resets them to their previous values at exit.

Usage::

    import contextvars, with_contextvars
    A = contextvars.ContextVar("A")
    B = contextvars.ContextVar("B")
    A.set("Hello,")
    B.set("world!")
    print(A.get(), B.get())
    # prints: Hello, world!
    with with_contextvars.Set((A, "other"), (B, "value")):
        print(A.get(), B.get())
        # prints: other value
    print(A.get(), B.get())
    # prints: Hello, world!

Even the entirety of variable assignments of a ``contextvars.Context`` object
(as obtained from ``contextvars.copy_context()``) can be activated by initializing
``Set`` with its items::

    with with_contextvars.Set(*context.items()):
        ...

However, using ``contextvars.Context.run()`` is more efficient and should be preferred
where possible.

More information can be found in the documentation of ``Set``.
