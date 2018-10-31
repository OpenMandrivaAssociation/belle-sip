%define major 0
%define devname %mklibname bellesip -d
%define libname %mklibname bellesip %major
%define __noautoreq '^libantlr3c\\.so.*$|^devel\\(libantlr3c(.*)$'

Name:           belle-sip
Version:        1.6.3
Release:        3
Summary:        Linphone sip stack

Group:          Communications
License:        GPL
URL:            http://www.linphone.org
Source0: 	https://www.linphone.org/snapshots/sources/%{name}/%{name}-%{version}.tar.gz
# https://github.com/antlr/website-antlr3/blob/gh-pages/download/antlr-3.4-complete.jar?raw=true
Source1:	antlr-3.4-complete.jar
# (wally) fix pkgconfig file contents when building with cmake
Patch0:		belle-sip-1.6.3-cmake-fix-pkgconfig-pc-file.patch
# (wally) allow overriding cmake config file location from cmd line
Patch1:		belle-sip-1.6.3-cmake-config-location.patch
BuildRequires:	antlr3-C-devel
BuildRequires:	pkgconfig(bctoolbox)
BuildRequires:	bctoolbox-static-devel
BuildRequires:	java
BuildRequires:	cmake
BuildConflicts:	antlr3-tool

%description
Belle-sip is an object oriented c written SIP stack used by Linphone.

%package -n %libname
Summary: The belle-sip library, a part of belle-sip
Group: System/Libraries
Requires: antlr3-C

%description -n %libname
The belle-sip library, a part of belle-sip.

%package -n %devname
Summary:       Development libraries for belle-sip
Group:         System/Libraries
Requires:      %{libname} = %{EVRD}
Requires:	antlr3-C-devel
Requires:	polarssl-devel

%description  -n %devname
Libraries and headers required to develop software with belle-sip

%prep
%setup -q
%apply_patches
cp %{SOURCE1} antlr.jar

#sed -i -e "s#antlr_java_prefixes=.*#antlr_java_prefixes=$PWD#" -e "s|-Werror||g" configure{,.ac}

%build
ANTLRJAR=`pwd`
%cmake \
    -DENABLE_STATIC:BOOL=NO \
    -DENABLE_STRICT:BOOL=NO \
    -DENABLE_TESTS=NO \
    -DANTLR3_JAR_PATH:PATH=$ANTLRJAR/antlr.jar \
    -DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/BelleSIP/

%make


%install
%makeinstall_std -C build

# remove static libraries
rm -f %{buildroot}%{_libdir}/libbellesip.a
rm -f %{buildroot}%{_libdir}/libbellesip.la

%files -n %devname
%{_includedir}/belle-sip
%{_libdir}/libbellesip.so
%{_libdir}/pkgconfig/belle-sip.pc
%{_libdir}/cmake/BelleSIP/
%files -n %libname
%{_libdir}/libbellesip.so.%{major}*
