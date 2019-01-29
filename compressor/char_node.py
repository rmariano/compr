"""compressor.char_node

This object represents a character being processed in the file, along with its
metadata, like the frequency of it (how many times it appears).
"""
from functools import total_ordering


@total_ordering
class CharNode:
    """
    Object that wraps/encapsulates the definition of a character
    in the text being processed.
    Used for comparison, and helper with its properties & methods.
    """

    def __init__(self, value, freq, left=None, right=None) -> None:
        """
        Represent a character as a node in a tree.

        :param value: the original character
        :param freq:  float with the occurrence average of `value`
                      in the processed text.
        :param left:  left child of this node.
        :param right: right child of this node in the tree.
        """
        self._value = value
        self.freq = freq
        self.left = left
        self.right = right

    def __le__(self, other) -> bool:
        """
        Compare if this character is less or equal than another
        one of the same kind.

        :param other: Another CharNode with properties.
        :return:      self <= other
        :rtype: bool
        """
        if self.__class__ is not other.__class__:
            return NotImplemented
        return self.freq <= other.freq

    def __eq__(self, other) -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return (self._value, self.freq) == (other.value, other.freq)

    def __hash__(self):
        return hash(self._value) ^ hash(self.freq)

    def __add__(self, other_node: "CharNode"):
        """Merge this node with the one received"""
        if not isinstance(other_node, self.__class__):
            raise TypeError(f"Incompatible type of {other_node!r}")
        return self._merge(self, other_node)

    __radd__ = __add__

    @classmethod
    def _merge(cls, left_node, right_node):
        return cls(
            value=f"{left_node.value}{right_node.value}",
            freq=left_node.freq + right_node.freq,
            left=left_node,
            right=right_node,
        )

    @property
    def value(self):
        """Expose the value being hold as read-only."""
        return self._value

    @property
    def leaf(self) -> bool:
        """
        Checks if the current node is a leaf in the tree. It is a leaf when it
        does not have any children (neither left nor right).

        :return: True if this node has no children, False otherwise.
        """
        return self.left is None and self.right is None
