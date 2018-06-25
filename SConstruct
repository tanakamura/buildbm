import sys
import kconfiglib
import os
import os.path
import menuconfig

from glob import glob

class Package:
    def __init__(self, package_dir, pkg_env):
        self.package_dir = package_dir
        self.pkg_env = pkg_env

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

    def config_get_str(name):
        node = kconf.syms[name]
        if node.type != kconfiglib.STRING:
            raise "{} is not string value".format(name)

        # substitute $(VAR)
        in_str = node.user_value
        out_str = ""
        i = 0

        while (i < len(in_str)) :
            if in_str[i] == '$' and in_str[i+1] == '(':
                i += 2
                begin = i

                while in_str[i] != ')':
                    i += 1

                end = i
                i+=1

                var_name = in_str[begin:end]

                out_str += kconf.syms[var_name].user_value
            else:
                out_str += in_str[i]
                i += 1

        return out_str

    packages = glob("packages/*/package.py")

    for i in packages:
        package_py = open(i).read()

        exec_env = {
            'config_get_bool' : config_get_bool,

            'PACKAGE_NAME' : None,
            'PACKAGE_URL' : None,
            'INSTALL_HEADERS' : None,
            'SOURCES' : None,
            'DEPENDENCIES' : None,
            'VERSION' : None,

            'CFLAGS' : None,
            'CXXFLAGS' : None
        }

        exec(compile(package_py, i, 'exec'),
             exec_env
        )

        build_packages = {}

        package_name = exec_env['PACKAGE_NAME']

        package_dir = os.path.dirname(i)

        if (package_name != None):
            build_packages[package_name] = Package(package_dir,exec_env)

    # xx : build dependency graph

    cc = config_get_str('BBM_TOOLCHAIN_CROSS_CC')
    cxx = config_get_str('BBM_TOOLCHAIN_CROSS_CXX')
    asm = config_get_str('BBM_TOOLCHAIN_CROSS_AS')
    ld = config_get_str('BBM_TOOLCHAIN_CROSS_LD')
    ar = config_get_str('BBM_TOOLCHAIN_CROSS_AR')

    build_env = Environment(
        ENV=os.environ,
        CC=cc,
        CXX=cxx,
        AS=asm,
        AR=ar,
        LD=ld
        )

    download_env = Environment()

    download_env.Decider('timestamp-match')

    c_source_list = []
    if 'BBM_TARGET_ARCH' in kconf.syms:
        target_arch = config_get_str('BBM_TARGET_ARCH')
    else:
        import platform
        target_arch = platform.machine()

    for pkg_name in build_packages:
        pkg_info = build_packages[pkg_name]

        pkg_info.output_dir = "output/%s/%s_%s"%(target_arch,
                                                 pkg_info.pkg_env['PACKAGE_NAME'],
                                                 pkg_info.pkg_env['VERSION'])

        url = pkg_info.pkg_env['PACKAGE_URL']
        dl_file = os.path.basename(url)
        dl_path = "dl/"+dl_file

        extract_dummy = os.path.join(pkg_info.output_dir, '.extract')

        Command(dl_path,
                '',
                ['wget -O %s %s'%(dl_path,url)])

        pkg_info.dl_path = dl_path

        Command(extract_dummy,
                dl_path,
                ['tar --strip-component=1  -C %s -zxf $SOURCE'%(pkg_info.output_dir),
                 Touch(extract_dummy)])

    for pkg_name in build_packages:
        pkg_info = build_packages[pkg_name]

        for csrc in pkg_info.pkg_env['SOURCES']:
            path_from_root = os.path.join(pkg_info.output_dir, csrc)
            c_source_list.append(path_from_root)

    objects = build_env.Object(c_source_list)
    build_env.StaticLibrary(os.path.join('output', target_arch, 'buildbm'), objects)

main()
