%define major 1
%define libname %mklibname bellesip
%define devname %mklibname bellesip -d

# exclude unwanted cmake requires
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$
%global __requires_exclude cmake\\(tunnel\\)|cmake\\(Tunnel\\)

%bcond_with	static
%bcond_with	strict
%bcond_with	tests

Name:		belle-sip
Version:	5.3.65
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

%files
%{_bindir}/%{name}-tester
%{_datadir}/%{name}-tester/

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
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_TESTS=%{?with_tests:ON}%{!?with_tests:OFF} \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/BelleSIP/ \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

