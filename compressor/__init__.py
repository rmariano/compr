"""compressor entry point"""
__version__ = "0.2.0"


from compressor.lib import compress_file, extract_file


__all__ = ["compress_file", "extract_file"]
