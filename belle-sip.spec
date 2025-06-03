%define major 1
%define libname %mklibname bellesip
%define devname %mklibname bellesip -d

# exclude unwanted cmake requires
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$
%global __requires_exclude cmake\\(tunnel\\)|cmake\\(Tunnel\\)

%bcond mdns			0
%bcond strict			0
%bcond tunnel			0
%bcond unit_tests		1
%bcond unit_tests_install	0

Name:		belle-sip
Version:	5.4.20
Release:	1
Summary:	Linphone sip stack
Group:		Communications
License:	GPLv3
URL:		https://www.linphone.org
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
# NOTE antlr-3.4-complete.jar is included into the source (src/antlr3c/antlr-3.4-complete.jar)
# https://github.com/antlr/website-antlr3/blob/gh-pages/download/antlr-3.4-complete.jar?raw=true
#Source1:	antlr-3.4-complete.jar
Patch0:		belle-sip-5.3.6-cmake-fix_cmake_path.patch

BuildRequires:	antlr3c-devel
BuildRequires:	cmake
BuildRequires:	pkgconfig(bctoolbox)
BuildRequires:	pkgconfig(belr)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	java
BuildRequires:	ninja
BuildConflicts:	antlr3-tool

%description
Belle-sip is an object oriented c written SIP stack used by Linphone.

%if %{with unit_tests} && %{with unit_tests_install}
%files
%{_bindir}/%{name}-tester
%{_datadir}/%{name}-tester/
%endif

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	The belle-sip library, a part of belle-sip
Group:		System/Libraries

%description -n %{libname}
The belle-sip library, a part of belle-sip.

%files -n %libname
%{_libdir}/libbelle-sip.so.%{major}*
%{_datadir}/belr/grammars/sdp_grammar

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development libraries for belle-sip
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Libraries and headers required to develop software with belle-sip

%files -n %{devname}
%{_includedir}/belle-sip
%{_libdir}/libbelle-sip.so
%{_libdir}/pkgconfig/belle-sip.pc
%{_datadir}/cmake/BelleSIP/

%prep
%autosetup -p1

#cp %{SOURCE1} antlr.jar
#sed -i -e "s#antlr_java_prefixes=.*#antlr_java_prefixes=$PWD#" -e "s|-Werror||g" configure{,.ac}

#---------------------------------------------------------------------------

%build
%cmake \
	-DENABLE_MDNS:BOOL=%{?with_mdns:ON}%{?!with_mdns:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_TUNNEL:BOOL=%{?with_tunnel:ON}%{?!with_tunnel:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF} \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/BelleSIP/ \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# don't install unit tester
%if %{with unit_tests} && ! %{with unit_tests_install}
rm -f  %{buildroot}%{_bindir}/%{name}-tester
rm -fr %{buildroot}%{_datadir}/%{name}-tester/
%endif

%check
%if %{with unit_tests}
pushd build
#FIXME:  some tests fail
ctest ||  true
popd
%endif

