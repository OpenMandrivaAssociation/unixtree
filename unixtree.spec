Name: unixtree
Version: 3.0.4
Release: 1
Source0: https://github.com/dokakod/unixtree/archive/refs/tags/v%{version}.tar.gz
Patch0: unixtree-3.0.4-clang-17.patch
Summary: Console-mode filemanager modeled after XTree Gold
URL: https://github.com/unixtree/unixtree
License: GPL-2.0
Group: System

%description
UnixTree is a powerful and versatile console-mode filemanager for Unix-style
systems, modeled very closely after the distinguished DOS program XTreeGold.

%prep
%autosetup -p1
sed -i -e 's,define TERM_SUBDIR.*,define TERM_SUBDIR "%{_libdir}/unixtree/trm/",g' libtcap/tcfndpth.c

%build
. ./build -r linux
# The Makefiles aren't SMP safe, can't use any form of -j
# (which %%make_build uses...)
make CDEFS="%{optflags}" BUILDER_NAM="OpenMandriva" BUILDER_EMA="team@openmandriva.org"

%install
. ./build -r linux
make install CDEFS="%{optflags}" INS_DIR=%{buildroot}%{_libdir}/unixtree

mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_datadir}
cd %{buildroot}%{_libdir}/unixtree
rm -rf catman
mv man %{buildroot}%{_datadir}
for i in *; do
	[ -f "$i" -a -x "$i" ] && mv "$i" %{buildroot}%{_bindir}/
done
ln -sf pcxterm-c.trm trm/xterm-256color.trm
ln -sf linux.trm trm/screen-256color.trm

%files
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/unixtree
