if config_get_bool("BBM_PACKAGE_ZLIB"):
    PACKAGE_NAME="zlib"
    PACKAGE_URL="http://prdownloads.sourceforge.net/libpng/zlib-1.2.11.tar.gz"

    VERSION='1.2.11'

    SOURCES=[
        "adler32.c",
        "compress.c",
        "crc32.c",
        "gzclose.c",
        "gzlib.c",
        "gzread.c",
        "gzwrite.c",
        "uncompr.c",
        "deflate.c",
        "trees.c",
        "zutil.c",
        "inflate.c",
        "infback.c",
        "inftrees.c",
        "inffast.c"
    ]

    INSTALL_HEADERS=[
        "zlib.h"
    ]