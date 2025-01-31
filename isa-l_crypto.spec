# doesn't seem to work on sles 12.3: %%{!?make_build:%%define make_build %%{__make} %%{?_smp_mflags}}
# so...
%if 0%{?suse_version} <= 1320
%define make_build  %{__make} %{?_smp_mflags}
%endif
%if 0%{?suse_version} >= 1315
%define isal_libname libisal_crypto2
%define isal_devname libisal_crypto-devel
%else
%define isal_libname libisa-l_crypto
%define isal_devname libisa-l_crypto-devel
%endif

Name:			isa-l_crypto
Version:	2.24.0
Release:	1%{?dist}

Summary:	Intelligent Storage Acceleration Library Crypto Version

%if 0%{?suse_version} >= 1315
Group: Development/Libraries/C and C++
%else
Group:		Development/Libraries
%endif
License:	BSD-3-Clause
URL:			https://github.com/01org/isa-l_crypto/wiki
Source0:	https://github.com/01org/%{name}/archive/isa-l_crypto-%{version}.tar.gz

BuildRequires: yasm

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool

%description
ISA-L_crypto is a collection of optimized low-level functions
targeting storage applications.

%package -n %{isal_libname}
Summary: Dynamic library for isa-l_crypto functions
License: BSD-3-Clause
Obsoletes: %{name} < %{version}

%description -n %{isal_libname}
ISA-L_crypto is a collection of optimized low-level functions
targeting storage applications. ISA-L_crypto includes:
- Multi-buffer hashes - run multiple hash jobs together on one core
for much better throughput than single-buffer versions. (
SHA1, SHA256, SHA512, MD5)
- Multi-hash - Get the performance of multi-buffer hashing with a
  single-buffer interface.
- Multi-hash + murmur - run both together.
- AES - block ciphers (XTS, GCM, CBC)
- Rolling hash - Hash input in a window which moves through the input

%package -n %{isal_devname}
Summary:	ISA-L_CRYPTO devel package
Requires:	%{isal_libname}%{?_isa} = %{version}
Provides:	%{isal_libname}-static%{?_isa} = %{version}

%description -n %{isal_devname}
Development files for the %{isal_libname} library.

%if (0%{?suse_version} > 0)
%global __debug_package 1
%global _debuginfo_subpackages 0
%debug_package
%endif

%prep
%autosetup -p1

%build
if [ ! -f configure ]; then
    ./autogen.sh --no-oshmem
fi
%configure --disable-static

%{make_build}

%install
%make_install
find %{?buildroot} -name *.la -print0 | xargs -r0 rm -f

%if 0%{?suse_version} >= 01315
%post -n %{isal_libname} -p /sbin/ldconfig
%postun -n %{isal_libname} -p /sbin/ldconfig
%else
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

%files -n %{isal_libname}
%{_libdir}/*.so.*

%files -n %{isal_devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libisal_crypto.pc

%changelog
* Thu Jun 22 2023 Brian J. Murrell <brian.murrell@intel> - 2.24.0-1
- Update to new version
- Disable static library build
- Add debuginfo generation for Leap 15

* Mon Feb 01 2021 Brian J. Murrell <brian.murrell@intel> - 2.23.0-1
- Update to new version
- Add %%{_libdir}/pkgconfig/libisal_crypto.pc to -devel package

* Wed Oct 02 2019 John E. Malmberg <john.e.malmberg@intel> - 2.21.0-3
- Fix the Red Hat family devel package name.

* Wed Oct 02 2019 John E. Malmberg <john.e.malmberg@intel> - 2.21.0-2
- Fix some SUSE rpmlint packaging complaints

* Fri Aug 16 2019 Ryon Jensen <ryon.jensen@intel> - 2.21.0-1
- initial package
