import sys
import kconfiglib
import os
import os.path
import menuconfig

from glob import glob

def main():
    kconf = kconfiglib.Kconfig("BMconfig")

    if os.path.exists(".config"):
        kconf.load_config(".config")
    else:
        menuconfig.menuconfig(kconf)

    def config_get_bool(name):
        node = kconf.syms[name]
        if node.type != kconfiglib.BOOL:
            raise "{} is not boolean value".format(name)

        return bool(node.user_value)

    packages = glob("packages/*/package.py")

    for i in packages:
        package_py = open(i).read()

        exec_env = {
            'config_get_bool' : config_get_bool,

            'PACKAGE_NAME' : None,
            'PACKAGE_URL' : None,
            'INSTALL_HEADERS' : None,
            'SOURCES' : None
            'DEPENDENCIES' : None

            'CFLAGS' : None
            'CXXFLAGS' : None
        }

        exec(compile(package_py, i, 'exec'),
             exec_env
        )

        package_name = exec_env['PACKAGE_NAME'] 
        if (package_name != None):
            build_packages[package_name] = exec_env

main()
