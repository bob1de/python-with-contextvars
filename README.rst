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
    with with_contextvars.Set((A, "other"), (B, "value")):
        print(A.get(), B.get())
        # prints: other value
    print(A.get(), B.get())
    # prints: Hello, world!

\... which is a shorthand for::

    t_A = A.set("other")
    t_B = B.set("value")
    try:
        ...
    finally:
        A.reset(t_A)
        B.reset(t_B)

Even the entirety of variable assignments of a ``contextvars.Context`` object (as
obtained from ``contextvars.copy_context()``) can be set this way::

    with with_contextvars.Set(*context.items()):
        ...

However, this should not be thought of as an equivalent of
``contextvars.Context.run()``, which runs code inside another context, while this
library applies variable assignments to the context currently active.

More information can be found in the documentation of ``Set``.
