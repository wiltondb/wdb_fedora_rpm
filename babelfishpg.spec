Name: babelfishpg
%global version_postgres_epoch 2
%global version_postgres_major 14
%global version_postgres_minor 5
Version: BABEL_2_2_0
%global version_postgres %{version_postgres_major}.%{version_postgres_minor}.%{version}
%global version_postgresql_modified_for_babelfish %{version}__PG_%{version_postgres_major}_%{version_postgres_minor}
Release: 1%{?dist}

Summary: Babelfish extensions for PostgreSQL
License: PostgreSQL
Url: https://babelfishpg.org/

Source0: %{version}.tar.gz
%global source0_sha512 a8ef0f95166695163edd900ab3592c4a3a4bce2600a9b12ffb2689f075ebc11947e1f6e20cef1c3884e944f7942f7179607cc106d75630d718c6d8d220fa5424
%global source0_url https://github.com/babelfish-for-postgresql/babelfish_extensions/archive/refs/tags/%{version}.tar.gz
Source1: %{version_postgresql_modified_for_babelfish}.tar.gz
%global source1_sha512 82ead048d6e3018062981db79820d72d910c78a1ae0a5a03c10dce49dc6b7d368c464f3a8bcd63b18a91d2cc7e67f530fb64d63a9c56f9408f322ab4ffd0894a
%global source1_url https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish/archive/refs/tags/%{version_postgresql_modified_for_babelfish}.tar.gz
	
Patch1: babelfishpg-antlr-4.10.patch
Patch2: babelfishpg-antlr-classpath.patch
Patch3: babelfishpg-cflags.patch
Patch4: babelfishpg-encoding-conversion.patch
 
BuildRequires: antlr4
BuildRequires: antlr4-cpp-runtime-devel
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: g++
BuildRequires: java-devel
BuildRequires: make
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
	wget -nv %{source0_url}
fi
echo "%{source0_sha512}  $(basename %{SOURCE0})" | sha512sum -c
if [ ! -s %{SOURCE1} ] ; then
	rm %{SOURCE1}
	wget -nv %{source1_url}
fi
echo "%{source1_sha512}  $(basename %{SOURCE1})" | sha512sum -c
popd

%setup -q -a 1 -n babelfish_extensions-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
	
%build
export cmake=cmake
export PG_CONFIG=/usr/bin/pg_config
export PG_SRC=`pwd`/postgresql_modified_for_babelfish-%{version_postgresql_modified_for_babelfish}

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
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.0.0--1.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.1.0--1.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.2.0--1.2.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.2.1--2.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.0.0--2.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.1.0--2.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
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
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
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
%{_datadir}/pgsql/extension/babelfishpg_common--1.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.0.0--1.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.1.0--1.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.2.0--1.2.1.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.2.1--2.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.0.0--2.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.1.0--2.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.2.0.sql
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
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql.control

%changelog
	
* Thu Dec 8 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-1
	
- Initial packaging of BABEL_2_2_0
