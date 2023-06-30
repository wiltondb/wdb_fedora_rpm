Name: babelfishpg
%global version_postgres_epoch 2
%global version_postgres_major 15
%global version_postgres_minor 3
Version: BABEL_3_2
%global version_postgres %{version_postgres_major}.%{version_postgres_minor}.%{version}
%global version_postgresql_modified_for_babelfish %{version}__PG_%{version_postgres_major}_%{version_postgres_minor}
%global version_postgresql_modified_for_babelfish_revision 9c4b78157a623a82f81f74f2e29c6b78bb3c9937
%global version_babelfish_extensions_revision c96f3c85d4a139e641fa88547df774241c616c23
Release: 1%{?dist}

Summary: Babelfish extensions for PostgreSQL
License: PostgreSQL
Url: https://babelfishpg.org/

Source0: %{version}.tar.gz
%global source0_sha512 375034baa2ecd0b71695c647d7a6f4179251b795821a1127303a64a31d88e19f2777bc19dd4db08e84ad4702199d19281c6241854dac3468fa47397ed1348b53
%global source0_url https://github.com/babelfish-for-postgresql/babelfish_extensions/archive/%{version_babelfish_extensions_revision}.tar.gz
Source1: %{version_postgresql_modified_for_babelfish}.tar.gz
%global source1_sha512 55cde0eb23c1a29fddff8e7236e598f9193b575c107b6eed74f8c6a7ecde923a92d6db14260f567eabb8e64a0bfc3839546ab44b52e074f17a67aaa11d509dce
%global source1_url https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish/archive/%{version_postgresql_modified_for_babelfish_revision}.tar.gz
	
Patch1: babelfishpg-cflags.patch
Patch2: babelfishpg-antlr-classpath.patch
Patch3: babelfishpg-antlr-4.10.patch
Patch4: babelfishpg-tds-warnings.patch
# https://github.com/babelfish-for-postgresql/babelfish_extensions/issues/997
Patch5: babelfishpg-sp_columns.patch
Patch6: babelfishpg-escape-hatch-type.patch

BuildRequires: antlr4
BuildRequires: antlr4-cpp-runtime-devel
BuildRequires: bison
BuildRequires: cmake
BuildRequires: flex
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: java-devel
BuildRequires: libxml2-devel
BuildRequires: make
BuildRequires: perl-lib
BuildRequires: perl-libs
BuildRequires: perl(FindBin)
BuildRequires: utf8cpp-devel
BuildRequires: wget

BuildRequires: postgresql-private-devel = %{version_postgres_epoch}:%{version_postgres}
BuildRequires: postgresql-server-devel = %{version_postgres_epoch}:%{version_postgres}

Requires: postgresql-server%{?_isa} = %{version_postgres_epoch}:%{version_postgres}
Requires: postgresql-contrib%{?_isa} = %{version_postgres_epoch}:%{version_postgres}
Requires: %{name}-money%{?_isa} = %{version}-%{release}
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Requires: %{name}-tds%{?_isa} = %{version}-%{release}
Requires: %{name}-tsql%{?_isa} = %{version}-%{release}
 
%description
Babelfish extensions add additional syntax, functions, data types, and more to PostgreSQL to help in the migration from SQL Server.

%package money
Summary: Supports the money type in MSSQL
%description money
This is a variation of the opensource fixeddecimal extension. FixedDecimal is a fixed precision decimal type which provides a subset of the features of PostgreSQL's builtin NUMERIC type, but with vastly increased performance. Fixeddecimal is targeted to cases where performance and disk space are a critical.

%package common
Summary: Supports the various datatypes in MSSQL
%description common
Supports NUMERIC, VARBINARY and other datatypes.

%package tds
Summary: Supports the TDS connection
%description tds
Supports Tabular Data Stream (TDS) protocol.

%package tsql
Summary: Supports the T-SQL language
%description tsql
Supports Transact-SQL (T-SQL) language.

%prep
pushd %{_sourcedir}
if [ ! -s %{SOURCE0} ] ; then
	rm %{SOURCE0}
	wget -nv %{source0_url} -O $(basename %{SOURCE0})
fi
echo "%{source0_sha512}  $(basename %{SOURCE0})" | sha512sum -c
if [ ! -s %{SOURCE1} ] ; then
	rm %{SOURCE1}
	wget -nv %{source1_url} -O $(basename %{SOURCE1})
fi
echo "%{source1_sha512}  $(basename %{SOURCE1})" | sha512sum -c
popd

%setup -q -a 1 -n babelfish_extensions-%{version_babelfish_extensions_revision}

%patch1 -p1
%patch2 -p1
%if ! 0%{?fc36}
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
export PG_CONFIG=/usr/bin/pg_config
export PG_SRC=`pwd`/postgresql_modified_for_babelfish-%{version_postgresql_modified_for_babelfish_revision}

# money
pushd ./contrib/babelfishpg_money/
make %{?_smp_mflags}
popd

# common
pushd ./contrib/babelfishpg_common/
make %{?_smp_mflags}
popd

# tds
pushd ./contrib/babelfishpg_tds/
make %{?_smp_mflags}
popd

# tsql
pushd ./contrib/babelfishpg_tsql/antlr
export ANTLR4_JAVA_BIN=/usr/bin/java
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo
%cmake_build
ln -s ./redhat-linux-build/antlr4cpp_generated_src
ln -s ./redhat-linux-build/libantlr_tsql.a
popd
pushd ./contrib/babelfishpg_tsql/
ln -s `pwd`/../babelfishpg_common/babelfishpg_common.so
make #%{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}%{_libdir}/pgsql
mkdir -p %{buildroot}%{_datadir}/pgsql/extension

# money
cp -p ./contrib/babelfishpg_money/babelfishpg_money.so %{buildroot}%{_libdir}/pgsql/
cp -p ./contrib/babelfishpg_money/babelfishpg_money--1.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_money/babelfishpg_money.control %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_money/fixeddecimal--1.0.0--1.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/

# common
cp -p ./contrib/babelfishpg_common/babelfishpg_common.so %{buildroot}%{_libdir}/pgsql/
pushd %{buildroot}%{_libdir}
    ln -s ./pgsql/babelfishpg_common.so babelfishpg_common.so
popd
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.0.0--1.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.1.0--1.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.2.0--1.2.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.2.1--2.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.0.0--2.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.1.0--2.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.2.0--2.3.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.3.0--2.4.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.3.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.4.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--3.0.0--3.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--3.1.0--3.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--3.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/babelfishpg_common.control %{buildroot}%{_datadir}/pgsql/extension/

# tds
cp -p ./contrib/babelfishpg_tds/babelfishpg_tds.so %{buildroot}%{_libdir}/pgsql/
cp -p ./contrib/babelfishpg_tds/babelfishpg_tds--1.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tds/babelfishpg_tds.control %{buildroot}%{_datadir}/pgsql/extension/

# tsql
cp -p ./contrib/babelfishpg_tsql/babelfishpg_tsql.so %{buildroot}%{_libdir}/pgsql/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.0.0--1.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.1.0--1.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.2.0--1.2.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.2.1--2.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.0.0--2.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.1.0--2.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.2.0--2.3.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.3.0--2.4.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.3.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.4.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--3.0.0--3.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--3.1.0--3.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--3.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/babelfishpg_tsql.control %{buildroot}%{_datadir}/pgsql/extension/

%files
%doc README.md
%license LICENSE.PostgreSQL
 
%files money
%{_libdir}/pgsql/babelfishpg_money.so
%{_datadir}/pgsql/extension/babelfishpg_money--1.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_money.control
%{_datadir}/pgsql/extension/fixeddecimal--1.0.0--1.1.0.sql

%files common
%{_libdir}/pgsql/babelfishpg_common.so
%{_libdir}/babelfishpg_common.so
%{_datadir}/pgsql/extension/babelfishpg_common--1.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.0.0--1.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.1.0--1.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.2.0--1.2.1.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.2.1--2.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.0.0--2.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.1.0--2.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.2.0--2.3.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.3.0--2.4.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.3.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.4.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--3.0.0--3.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--3.1.0--3.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--3.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common.control

%files tds
%{_libdir}/pgsql/babelfishpg_tds.so
%{_datadir}/pgsql/extension/babelfishpg_tds--1.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tds.control

%files tsql
%{_libdir}/pgsql/babelfishpg_tsql.so
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.0.0--1.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.1.0--1.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.2.0--1.2.1.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.2.1--2.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.0.0--2.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.1.0--2.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.2.0--2.3.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.3.0--2.4.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.3.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.4.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--3.0.0--3.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--3.1.0--3.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--3.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql.control

%changelog
* Fri Jun 30 2023 Alex Kasko <alex@staticlibs.net> - BABEL_3_2-1
- Update to BABEL_3_2_STABLE (c96f3c8)

* Tue May  9 2023 Alex Kasko <alex@staticlibs.net> - BABEL_3_1-2
- UTF8-CPP usage fix with ANTLR

* Mon May  8 2023 Alex Kasko <alex@staticlibs.net> - BABEL_3_1-1
- Update to BABEL_3_1_STABLE (28aa208)

* Tue Mar  7 2023 Alex Kasko <alex@staticlibs.net> - BABEL_2_3_0-4
- SQL patches for JDBC introspection, clean extension install only

* Wed Feb 15 2023 Alex Kasko <alex@staticlibs.net> - BABEL_2_3_0-3
- Update to the same upstream tag that was re-created on different commit

* Mon Jan 30 2023 Alex Kasko <alex@staticlibs.net> - BABEL_2_3_0-2
- Disable ANTLR headers warning with GCC 13

* Fri Jan 27 2023 Alex Kasko <alex@staticlibs.net> - BABEL_2_3_0-1
- Update to BABEL_2_3_0

* Thu Dec 29 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_1-1
- Update to BABEL_2_2_1

* Fri Dec 23 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-4
- Use utf8cpp instead of codecvt with antlr C++ runtime

* Tue Dec 20 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-3
- Use cmake directly when building TSQL module

* Sat Dec 17 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-2
- Full working build
	
* Thu Dec 8 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-1
- Initial packaging of BABEL_2_2_0
