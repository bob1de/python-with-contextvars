"""
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
"""

import typing as T

import contextvars


__all__ = ("Set",)
__version__ = "0.1.2"


class Set:
    """
    A context manager which performs ``contextvars`` variable assignments and resets.

    Any number of two-tuples may be passed at initialization, where the first element
    is a ``contextvars.ContextVar`` instance and the second is the value to set for
    that variable.
    Multiple instances may also be combined using the + operator, resulting in a
    context manager performing the variable assignments of all instances in order.

    If desired, the same instance can be re-used after the previous ``with`` block
    using it was left.
    A ``RuntimeError`` is raised when trying to enter an instance already active.
    """

    __slots__ = ("_assignments", "_tokens")

    def __init__(self, *assignments: T.Tuple[contextvars.ContextVar, T.Any]):
        self._assignments = assignments
        self._tokens: T.Optional[T.Tuple[contextvars.Token]] = None

    def __add__(self, other: "Set") -> "Set":
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)(*self._assignments, *other._assignments)

    def __enter__(self):
        if self._tokens is not None:
            raise RuntimeError("{!r} is already active".format(self))
        self._tokens = tuple(var.set(value) for var, value in self._assignments)

    def __exit__(self, *args):
        for token in reversed(self._tokens):
            token.var.reset(token)
        self._tokens = None

    def __repr__(self):
        return "<{}.{} ({}active) : {}>".format(
            type(self).__module__,
            type(self).__qualname__,
            "in" if self._tokens is None else "",
            ", ".join(
                "{}={!r}".format(var.name, value) for var, value in self._assignments
            ),
        )

    @property
    def assignments(self) -> T.Tuple[T.Tuple[contextvars.ContextVar, T.Any], ...]:
        """Tuple of context variable assignments this context manager performs."""
        return self._assignments

    @property
    def is_active(self) -> bool:
        """Whether this context manager is currently active."""
        return self._tokens is not None
