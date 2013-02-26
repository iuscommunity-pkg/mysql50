
# don't build with cluster by default
#%%define _with_cluster 1

%define with_cluster %{?_with_cluster:1}%{!?_with_cluster:0}
%define basever 5.0
%define real_name mysql
%define name mysql50

Name: %{name}
Version: 5.0.96
Release: 2.ius%{?dist}
Summary: MySQL client programs and shared libraries.
License: GPL
Vendor: IUS Community Project 
Group: Applications/Databases
URL: http://www.mysql.com

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest:%define runselftest 1}

Source0: http://dev.mysql.com/get/Downloads/MySQL-5.0/mysql-%{version}.tar.gz
Source1: mysql.init
Source8: mysql.init.old
Source2: mysql.logrotate
Source3: my.cnf-stock

Source4: scriptstub.c
Source5: my_config.h
Source6: my-psa.cnf
Source9: my-50-terse.cnf
Source10: my-50-verbose.cnf
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh 
Patch201: mysql-5.0.27-libdir.patch
Patch2: mysql-errno.patch
Patch303: mysql-5.0.33-libtool.patch
Patch304: mysql-5.0.37-testing.patch
Patch205: mysql-5.0.27-no-atomic.patch
Patch6: mysql-rpl_ddl.patch
Patch7: mysql-rpl-test.patch
Patch9: mysql-bdb-link.patch
Patch10: mysql-strmov.patch
Patch13: mysql-no-dbug.patch
Patch15: mysql-stack-guard.patch
Patch22: mysql-cve-2010-1626.patch
# Applied by upstream
#Patch24: mysql-cve-2010-3677.patch
Patch25: mysql-cve-2010-3680.patch
Patch26: mysql-5.0.91-cve-2010-3681.patch
# Applied by upstream
#Patch27: mysql-cve-2010-3682.patch
#Patch28: mysql-cve-2010-3833.patch
#Patch29: mysql-5.0.91-cve-2010-3835.patch
#Patch30: mysql-cve-2010-3836.patch
#Patch31: mysql-cve-2010-3837.patch
#Patch32: mysql-cve-2010-3838.patch
Patch33: mysql-cve-2010-3839.patch
#Patch34: mysql-cve-2010-3840.patch
Patch207: mysql-5.0.41-compress-test.patch 
Patch208: mysql-5.0.67-mysqld_safe.patch 
Patch209: mysql-5.0.67-bindir.patch
#Patch217: mysql-5.0.75-automake_el3.patch
#Patch316: mysql-5.1.43-ssl_cert.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires(pre): /sbin/ldconfig, /sbin/install-info, grep, fileutils, chkconfig
BuildRequires: gperf, perl, readline-devel, openssl-devel
BuildRequires: gcc-c++, ncurses-devel, zlib-devel
BuildRequires: libtool automake autoconf, gcc
Requires: bash
Obsoletes: mysql-client mysql-perl
Conflicts: MySQL

Provides:  %{real_name} = %{version}-%{release}
Conflicts: %{real_name} < %{basever}
Conflicts: mysql51

# Not compatible with Plesk 8.1 (Rackspace-ism)
Conflicts: psa < 8.1


# make test requires time
BuildRequires: time

# Good for Rhel3/Rhel4 both
%if 0%{?el4}
Requires: mysqlclient10 mysqlclient10-devel
requires: mysqlclient14 mysqlclient14-devel
%endif

BuildRequires: gettext-devel


# Working around perl dependency checking bug in rpm FTTB. Remove later.
%define __perl_requires %{SOURCE999}

%description
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the MySQL client programs, the client shared libraries, and
generic MySQL files.

%package server

Summary:    The MySQL server and related files.
License:    GPL
Group:      Applications/Databases
Requires(pre):     /sbin/chkconfig, /usr/sbin/useradd
Requires:   %{name} = %{version}-%{release}, sh-utils
# mysqlhotcopy needs DBI/DBD support
Requires:   perl-DBI, perl-DBD-MySQL
Conflicts:  MySQL-server
Provides:   %{real_name}-server = %{version}-%{release}
Conflicts:  %{real_name}-server < %{base_ver}
Conflicts:  mysql51-server

%description server
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MySQL server and some accompanying files and directories.

%package devel

Summary:    Files for development of MySQL applications.
License:    GPL
Group:      Applications/Databases
Requires:   %{name} = %{version}-%{release}
Requires:   openssl-devel
Conflicts:  MySQL-devel
Provides:   %{real_name}-devel = %{version}-%{release}
Conflicts:  %{real_name}-devel < %{base_ver}
Conflicts:  mysql51-devel

%description devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the libraries and header files that are needed for
developing MySQL client applications.

%package bench

Summary:    MySQL benchmark scripts and data.
License:    GPL
Group:      Applications/Databases
Requires:   %{name} = %{version}-%{release}
Conflicts:  MySQL-bench
Provides:   %{real_name}-bench = %{version}-%{release}
Conflicts:  %{real_name}-bench < %{base_ver}
Conflicts:  mysql51-bench

%description bench
MySQL is a multi-user, multi-threaded SQL database server. This
package contains benchmark scripts and data for use when benchmarking
MySQL.

%if %{with_cluster}
%package    clusterstorage
Summary:    MySQL - ndbcluster storage engine
Group:      Applications/Databases
Obsoletes:  ndb-storage
Conflicts:  MySQL-clusterstorage
Requires:   %{name} = %{version}-%{release}, %{name}-server = %{version}-%{release}
Provides:   %{real_name}-clusterstorage = %{version}-%{release}
Conflicts:  %{real_name}-clusterstorage < %{base_ver}
Conflicts:  mysql51-clusterstorage

%description clusterstorage
This package contains the ndbcluster storage engine.
It is necessary to have this package installed on all
computers that should store ndbcluster table data.
Note that this storage engine can only be used in conjunction
with the MySQL Max server.

%package    clustermanagement
Summary:    MySQL - ndbcluster storage engine management
Group:      Applications/Databases
Obsoletes:  ndb-management
Conflicts:  MySQL-clustermanagement
Requires:   %{name} = %{version}-%{release}, %{name}-server = %{version}-%{release}
Provides:   %{real_name}-clustermanagement = %{version}-%{release}
Conflicts:  %{real_name}-clustermanagement < %{base_ver}
Conflicts:  mysql51-clustermanagement

%description clustermanagement
This package contains ndbcluster storage engine management.
It is necessary to have this package installed on at least
one computer in the cluster.

%package    clustertools
Summary:    MySQL - ndbcluster storage engine basic tools
Group:      Applications/Databases
Obsoletes:  ndb-tools
Provides:   ndb-tools,
Conflicts:  MySQL-clustertools
Requires:   %{name} = %{version}-%{release}, %{name}-server = %{version}-%{release}
Provides:   %{real_name}-clustertools = %{version}-%{release}
Conflicts:  %{real_name}-clustertools < %{base_ver}
Conflicts:  mysql51-clustertools

%description clustertools
This package contains ndbcluster storage engine basic tools.

%package    clusterextra
Summary:    MySQL - ndbcluster storage engine extra tools
Group:      Applications/Databases
Obsoletes:  ndb-extra
Requires:   %{name} = %{version}-%{release}, %{name}-server = %{version}-%{release}
Provides:   %{real_name}-clusterextra = %{version}-%{release}
Conflicts:  %{real_name}-clusterextra < %{base_ver}
Conflicts:  mysql51-clusterextra


%description clusterextra
This package contains some extra ndbcluster storage engine tools for the advanced user.
They should be used with caution.

%endif # with_cluster



%prep
%setup -q -n %{real_name}-%{version} 


cp %SOURCE9 .
cp %SOURCE10 .
    
sed -i "s|@@@mysql_server_docdir@@@|%{_docdir}|" my-50-terse.cnf
sed -i "s|@@@mysql_server_docdir@@@|%{_docdir}|" my-50-verbose.cnf

%patch201 -p1
%patch2 -p1
%patch303 -p1 
%patch304 -p1
%patch205 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1 -b .bdb-link
%patch10 -p1 -b .strmov
%patch13 -p1 -b .no-dbug
%patch15 -p1 -b .stack-guard
%patch22 -p1 -b .cve-2010-1626
#%patch24 -p1 -b .cve-2010-3677
%patch25 -p1 -b .cve-2010-3680
%patch26 -p1 -b .cve-2010-3681
#%patch27 -p1 -b .cve-2010-3682
#%patch28 -p1 -b .cve-2010-3833
#%patch29 -p1 -b .cve-2010-3835
#%patch30 -p1 -b .cve-2010-3836
#%patch31 -p1 -b .cve-2010-3837
#%patch32 -p1 -b .cve-2010-3838
%patch33 -p1 -b .cve-2010-3839
#%patch34 -p1 -b .cve-2010-3840
%patch207 -p1  
%patch208 -p1 -b .mysqld_safe
%patch209 -p1 -b .bindir
#%patch217 -p1 -b .automake_el3

libtoolize --force
aclocal
automake

autoconf
autoheader

%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# MySQL 4.1.10 definitely doesn't work under strict aliasing; also,
# gcc 4.1 breaks MySQL 5.0.16 without -fwrapv
CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"

# Also Resolved MySQL Bug: #18091 and #19999
# same as MySQL builds... always build as
# position indipendant code.
CFLAGS="$CFLAGS -fPIC"

CXXFLAGS="$CFLAGS -felide-constructors -fno-rtti -fno-exceptions"
export CFLAGS CXXFLAGS

%configure \
	--with-readline \
    --with-comment='Distributed by The IUS Community Project' \
    --with-server-suffix='-ius' \
	--with-openssl \
	--without-debug \
	--enable-shared \
	--with-bench \
	--localstatedir=/var/lib/mysql \
	--with-unix-socket-path=/var/lib/mysql/mysql.sock \
	--with-mysqld-user="mysql" \
	--with-extra-charsets=all \
	--with-innodb \
	--with-berkeley-db \
	--enable-local-infile \
	--enable-largefile \
    --enable-community-features \
	--enable-profiling \
	--enable-thread-safe-client \
	--disable-dependency-tracking \
    --with-archive-storage-engine \
    --with-federated-storage-engine \
    --with-blackhole-storage-engine \
    --with-csv-storage-engine \
    %{?_with_cluster:--with-extra-charsets=all} \
    %{?_with_cluster:--with-ndbcluster} \
	--with-named-thread-libs="-lpthread"

gcc $CFLAGS $LDFLAGS -o scriptstub "-DLIBDIR=\"%{_libdir}/mysql\"" %{SOURCE4}
make %{?_smp_mflags}
make check

# Fix for builds, these files exist without the 'cve' suffix... but weren't deleted, only chmod'd 0000
rm -f mysql-test/suite/innodb/t/innodb_bug54044.test.cve-2010-3680
rm -f mysql-test/suite/innodb/r/innodb_bug54044.result.cve-2010-3680

%if %runselftest
  make test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with_cluster}
# Create cluster directory if needed
mkdir -p ${RPM_BUILD_ROOT}/var/lib/mysql-cluster
%endif


%makeinstall
install -m 644 include/my_config.h $RPM_BUILD_ROOT/usr/include/mysql/my_config_`uname -i`.h
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/usr/include/mysql/
mkdir -p $RPM_BUILD_ROOT/var/log
touch $RPM_BUILD_ROOT/var/log/mysqld.log

# List the installed tree for RPM package maintenance purposes.
find $RPM_BUILD_ROOT -print | sed "s|^$RPM_BUILD_ROOT||" | sort > ROOTFILES
gzip ${RPM_BUILD_ROOT}%{_infodir}/*
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql-*.spec
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql-log-rotate

mkdir -p $RPM_BUILD_ROOT/etc/{rc.d/init.d,logrotate.d}
mkdir -p $RPM_BUILD_ROOT/var/run/mysqld
mkdir -p $RPM_BUILD_ROOT/var/lib/mysqllogs
mkdir -p $RPM_BUILD_ROOT/var/lib/mysqltmp

install -m 0755 -d $RPM_BUILD_ROOT/var/lib/mysql
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mysqld

install -m 0644 support-files/mysql.server $RPM_BUILD_ROOT/etc/rc.d/init.d/mysqld-lsb
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/mysqld
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT/etc/my.cnf

install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT/etc/my-psa.cnf
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir*
mv $RPM_BUILD_ROOT/usr/sql-bench $RPM_BUILD_ROOT%{_datadir}/sql-bench

mv ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysqlbug
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug
mv ${RPM_BUILD_ROOT}%{_bindir}/mysql_config ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysql_config
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

rm -fr $RPM_BUILD_ROOT/usr/mysql-test
rm -f ${RPM_BUILD_ROOT}%{_bindir}/*client_test
rm -f ${RPM_BUILD_ROOT}%{_bindir}/comp_err
rm -f ${RPM_BUILD_ROOT}%{_bindir}/make_win_binary_distribution
rm -f ${RPM_BUILD_ROOT}%{_bindir}/make_win_src_distribution
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient*.la
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/binary-configure
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/make_binary_distribution
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/make_sharedlib_distribution
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mi_test_all*
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/*.cnf
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/*.ini
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql.server
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/MySQL-shared-compat.spec
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/*.plist
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/preinstall
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/postinstall

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/mysql" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre 
# This is to remind everyone to run fix_privilege_tables
curMySQLVersion=$(mysql_config --version 2> /dev/null | awk -F . {' print $1"."$2 '})
newMySQLVersion=$(echo %{version} | awk -F . {' print $1"."$2 '})

curIsLessThanNew=$(echo "$curMySQLVersion $newMySQLVersion" | awk '{if ($1 < $2) print "true"}')
if [ $curIsLessThanNew ]; then 
cat <<EOF
========================================================================

    Please note that if you are upgrading major versions of MySQL 
    you must run the following script:

    %{_bindir}/mysql_upgrade -t /tmp

========================================================================
EOF

fi


%pre server
/usr/sbin/groupadd -g 27 mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -o -r -d /var/lib/mysql -s /bin/bash \
	-c "MySQL Server" -u 27 mysql -g mysql > /dev/null 2>&1 || :



%post 
/sbin/install-info %{_infodir}/mysql.info.gz %{_infodir}/dir
/sbin/ldconfig


%post server
if [ $1 = 1 ]; then
    /sbin/chkconfig --add mysqld
fi
if [ $1 -ge 1 ]; then
    /sbin/service mysqld condrestart || :
fi
/bin/chmod 0755 /var/lib/mysql
/bin/touch /var/log/mysqld.log



%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/mysql.info.gz %{_infodir}/dir
fi

%preun server
if [ $1 = 0 ]; then
    /sbin/service mysqld stop || :
    /sbin/chkconfig --del mysqld
fi

%postun
if [ $1 = 0 ] ; then
    /sbin/ldconfig
fi


%postun server
if [ $1 = 0 ] ; then
	userdel mysql >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root)
%doc README COPYING

%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysql_config
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_tableinfo
%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqldumpslow
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow

%{_infodir}/*

%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlbug.1.gz
%dir %{_libdir}/mysql
%{_libdir}/mysql/libmysqlclient*.so.*
%{_libdir}/mysql/mysqlbug
%{_libdir}/mysql/mysql_config
/etc/ld.so.conf.d/*

%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%lang(cs) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(nl) %{_datadir}/mysql/dutch
%lang(et) %{_datadir}/mysql/estonian
%lang(fr) %{_datadir}/mysql/french
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(ja) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(no) %{_datadir}/mysql/norwegian
%lang(no) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ro) %{_datadir}/mysql/romanian
%lang(ru) %{_datadir}/mysql/russian
%lang(sr) %{_datadir}/mysql/serbian
%lang(sk) %{_datadir}/mysql/slovak
%lang(es) %{_datadir}/mysql/spanish
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian
%{_datadir}/mysql/charsets
%config(noreplace) /etc/my.cnf
/etc/my-psa.cnf

%files server
%defattr(-,root,root)
%doc support-files/*.cnf
%doc my-50-terse.cnf my-50-verbose.cnf 

%if %{with_cluster}
%doc support-files/ndb-*.ini
%endif

%{_datadir}/mysql/mysqld_multi.server
%{_bindir}/my_print_defaults
%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_explain_log
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_fix_privilege_tables
%{_bindir}/mysql_install_db
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_zap
%{_bindir}/mysqlbug
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe
%{_bindir}/mysqlhotcopy
%{_bindir}/mysqltestmanager
%{_bindir}/mysqltestmanager-pwgen
%{_bindir}/mysqltestmanagerc
%{_bindir}/mysqltest
%{_bindir}/innochecksum
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip
%{_bindir}/mysql_upgrade
%{_bindir}/mysql_upgrade_shell

/usr/libexec/*

%{_mandir}/man1/msql2mysql.1.gz
%{_mandir}/man1/myisamchk.1.gz
%{_mandir}/man1/myisamlog.1.gz
%{_mandir}/man1/myisampack.1.gz
%{_mandir}/man1/mysql.server.1.gz
%{_mandir}/man1/mysql_config.1.gz
%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlbinlog.1.gz
%{_mandir}/man1/mysqlcheck.1.gz
%{_mandir}/man1/my_print_defaults.1.gz
%{_mandir}/man1/mysql_install_db.1.gz
%{_mandir}/man1/mysql_tzinfo_to_sql.1.gz
%{_mandir}/man1/mysqlhotcopy.1.gz
%{_mandir}/man1/mysqlimport.1.gz
%{_mandir}/man1/mysqlman.1.gz
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/safe_mysqld.1*
%{_mandir}/man1/myisam_ftdump.1.gz
%{_mandir}/man1/mysql_explain_log.1.gz
%{_mandir}/man1/mysql_upgrade.1.gz
%{_mandir}/man8/mysqld.8.gz
%{_mandir}/man8/mysqlmanager*.gz
%{_mandir}/man1/mysqld_multi.1.gz
%{_mandir}/man1/mysqld_safe.1.gz
%{_mandir}/man1/comp_err.1.gz
%{_mandir}/man1/innochecksum.1.gz
%{_mandir}/man1/mysql-stress-test.pl.1.gz
%{_mandir}/man1/mysql-test-run.pl.1.gz
%{_mandir}/man1/mysql_client_test.1.gz
%{_mandir}/man1/mysql_convert_table_format.1.gz
%{_mandir}/man1/mysql_find_rows.1.gz
%{_mandir}/man1/mysql_fix_extensions.1.gz
%{_mandir}/man1/mysql_secure_installation.1.gz
%{_mandir}/man1/mysql_setpermission.1.gz
%{_mandir}/man1/mysql_tableinfo.1.gz
%{_mandir}/man1/mysql_waitpid.1.gz
%{_mandir}/man1/mysqltest.1.gz
%{_mandir}/man1/resolve_stack_dump.1.gz
%{_mandir}/man1/resolveip.1.gz

   

%dir %{_datadir}/mysql
%{_datadir}/mysql/errmsg.txt
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
/etc/rc.d/init.d/mysqld-lsb
/etc/rc.d/init.d/mysqld
%attr(0755,mysql,mysql) %dir /var/run/mysqld
%attr(0750,mysql,mysql) %dir /var/lib/mysqllogs
%attr(0750,mysql,mysql) %dir /var/lib/mysqltmp
%config(noreplace) /etc/logrotate.d/mysqld
%attr(0755,mysql,mysql) %dir /var/lib/mysql
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /var/log/mysqld.log

%files devel
%defattr(-,root,root)
/usr/include/mysql
%dir %{_libdir}/mysql
%{_libdir}/mysql/*.a
%{_libdir}/mysql/libmysqlclient*.so

%if %{with_cluster}
%{_libdir}/mysql/libndbclient.la
%endif

%files bench
%defattr(-,root,root)
%{_datadir}/sql-bench


%if %{with_cluster}
%files clusterstorage
%defattr(-,root,root)
%attr(755, root, root) %{_prefix}/libexec/ndbd
%attr(644, root, root) %{_libdir}/mysql/libndbclient.so*
%attr(644, root, man) %{_mandir}/man1/ndb_print*file.1*
%attr(644, root, man) %{_mandir}/man8/ndb_mgmd.8.gz
%attr(644, root, man) %{_mandir}/man8/ndbd.8.gz


%files clustermanagement
%defattr(-,root,root)
%attr(755, root, root) %{_prefix}/libexec/ndb_mgmd

%files clustertools
%defattr(-,root,root)
%attr(755, root, root) %{_bindir}/ndb_config
%attr(755, root, root) %{_bindir}/ndb_desc
%attr(755, root, root) %{_bindir}/ndb_error_reporter
%attr(755, root, root) %{_bindir}/ndb_mgm
%attr(755, root, root) %{_bindir}/ndb_restore
%attr(755, root, root) %{_bindir}/ndb_select_all
%attr(755, root, root) %{_bindir}/ndb_select_count
%attr(755, root, root) %{_bindir}/ndb_show_tables
%attr(755, root, root) %{_bindir}/ndb_size.pl
%attr(755, root, root) %{_bindir}/ndb_test_platform
%attr(755, root, root) %{_bindir}/ndb_waiter
%attr(-, root, root) %{_datadir}/mysql/ndb_size.tmpl
%attr(644, root, man) %{_mandir}/man1/ndb_config.1*
%attr(644, root, man) %{_mandir}/man1/ndb_desc.1*
%attr(644, root, man) %{_mandir}/man1/ndb_error_reporter.1*
%attr(644, root, man) %{_mandir}/man1/ndb_mgm.1*
%attr(644, root, man) %{_mandir}/man1/ndb_restore.1*
%attr(644, root, man) %{_mandir}/man1/ndb_select_all.1*
%attr(644, root, man) %{_mandir}/man1/ndb_select_count.1*
%attr(644, root, man) %{_mandir}/man1/ndb_show_tables.1*
%attr(644, root, man) %{_mandir}/man1/ndb_size.pl.1*
%attr(644, root, man) %{_mandir}/man1/ndb_waiter.1*

%files clusterextra
%defattr(-,root,root)
%attr(755, root, root) %{_bindir}/ndb_delete_all
%attr(755, root, root) %{_bindir}/ndb_drop_index
%attr(755, root, root) %{_bindir}/ndb_drop_table
%attr(755, root, root) %{_prefix}/libexec/ndb_cpcd
%attr(644, root, man) %{_mandir}/man1/ndb_delete_all.1*
%attr(644, root, man) %{_mandir}/man1/ndb_drop_index.1*
%attr(644, root, man) %{_mandir}/man1/ndb_drop_table.1*
%attr(644, root, man) %{_mandir}/man1/ndb_cpcd.1*
%endif


%changelog
* Wed May 02 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.0.96-2.ius
- Removing libpcap Requires per https://bugs.launchpad.net/ius/+bug/992718

* Thu Mar 22 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.0.96-1.ius
- Latest sources from upstream

* Wed Feb 22 2012 BJ Dierkes <wdierkes@rackspace.com> - 5.0.95-2.ius
- Re-enable testing
- Delete troublesome test files in %%prep
- Remove all el3 hacks as we do not support el3.

* Mon Feb 13 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.0.95-1.ius
- Latest sources from upstream
- Removing Patch34 as it is applied upstream

* Wed Feb 09 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.0.92-1.ius
- Final sources from upstream for mysql 5.0:
  http://dev.mysql.com/doc/refman/5.0/en/news-5-0-92.html
- CVEs addressed by update:
  CVE-2010-3833 CVE-2010-3834 CVE-2010-3835 CVE-2010-3677 
  CVE-2010-3836 CVE-2010-3837 CVE-2010-3838 CVE-2010-3682 
- Removed: Patch24: mysql-cve-2010-3677.patch
- Removed: Patch27: mysql-cve-2010-3682.patch
- Removed: Patch28: mysql-cve-2010-3833.patch
- Removed: Patch29: mysql-5.0.91-cve-2010-3835.patch
- Removed: Patch30: mysql-cve-2010-3836.patch
- Removed: Patch31: mysql-cve-2010-3837.patch
- Removed: Patch32: mysql-cve-2010-3838.patch
- Removed: %%doc EXCEPTIONS-CLIENT as it was 
  removed from upstream source

* Wed Nov 10 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.0.91-3.ius
- Change 'prereq' references to use Requires(pre)
- Removed hack to copy in system mkinstalldirs
- Backup-up-porting patches from Redhat
- Adding Patch9: mysql-bdb-link.patch
- Adding Patch10: mysql-strmov.patch
- Adding Patch13: mysql-no-dbug.patch
- Adding Patch15: mysql-stack-guard.patch
- Adding Patch22: mysql-cve-2010-1626.patch
- Adding Patch24: mysql-cve-2010-3677.patch
- Adding Patch25: mysql-cve-2010-3680.patch
- Adding Patch26: mysql-5.0.91-cve-2010-3681.patch
- Adding Patch27: mysql-cve-2010-3682.patch
- Adding Patch28: mysql-cve-2010-3833.patch
- Adding Patch29: mysql-5.0.91-cve-2010-3835.patch
- Adding Patch30: mysql-cve-2010-3836.patch
- Adding Patch31: mysql-cve-2010-3837.patch
- Adding Patch32: mysql-cve-2010-3838.patch
- Adding Patch33: mysql-cve-2010-3839.patch
- Adding Patch34: mysql-cve-2010-3840.patch

* Thu Jun 24 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.0.91-2.ius
- Rebuild against 'i386' mock config

* Fri May 21 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.0.91-1.ius
- Latest sources from upstream.  Full changelog available at:
  http://dev.mysql.com/doc/refman/5.0/en/news-5-0-91.html
- This update includes security fixes for the following:
  CVE-2010-1848, CVE-2010-1850, CVE-2010-1849.
- Removed Patch316: mysql-5.1.43-ssl_cert.patch (applied upstream)

* Mon Feb 01 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.0.90-1.ius
- Latest sources from upstream.
- Added Patch316: mysql-5.1.43-ssl_cert.patch

* Tue Jan 05 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.0.89-1.ius
- Latest sources from upstream, resolves LP#499202
- Explicity set -g 27 guid when adding mysql group, resolves LP#499650

* Wed Dec 16 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.88-3.ius
- Install my-50-verbose as default my.cnf

* Tue Dec 01 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.88-2.ius
- No longer provide mysqlclient/mysqlclient-devel (regression)
  resolves LP #490983

* Tue Nov 23 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.88-1.ius
- Latest sources from upstream.
- Removed Patch223: mysql-5.0.85-disabled-tests.patch
- Added /var/lib/mysqltmp dir

* Tue Nov 17 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.87-1.ius
- Latest sources from upstream.  Resolves LP #483901.

* Tue Oct 06 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.86-1.ius
- Latest sources from upstream.

* Wed Oct 01 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.85-1.1.ius
- Rebuilding for EL4/EL5
- Provides: mysqlclient15{-devel} (again)

* Mon Aug 31 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.85-1.ius
- Latest sources from upstream
- Updating default my.cnf a tad
- Adding SOURCE9(my-50-terse.cnf) and SOURCE10(my-50-verbose.cnf) to
  doc dir.
- Removed Patch221: mysql-5.0.84-disabled_tests.patch
- Added Patch223: mysql-5.0.85-disabled-tests.patch

* Mon Aug 03 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.84-1.ius
- Latest sources from upstream
- Changing comment line for 'The IUS Community Project'
- On %post(server) do a condrestart rather than restart
- Explicitly add the mysql group in %post (before the mysql user 
  is added)
- Replaced Patch221: mysql-5.0.81-disabled_tests.patch with
  mysql-5.0.84-disabled_tests.patch
- Removed Patch222: mysql-5.0.83-bug45236.patch (applied upstream)
- No longer Obscolete/Provide mysqlclient15{-devel}

* Thu Jul 23 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.83-2.ius
- Repackaged for IUS

* Thu Jul 09 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.83-1.2.rs
- Adding --enable-community-features and --enable-profiling

* Tue Jun 22 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.83-1.1.rs
- Added Patch222: mysql-5.0.83-bug45236.patch

* Mon Jun 22 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.83-1.rs
- Latest sources from upstream.

* Mon May 11 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.81-1.2.rs
- No longer send output of init script to /dev/null.

* Wed May 06 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.81-1.1.rs
- Updated mysql.init script to be inline with current EL5 script.
- Added Patch221: mysql-5.0.81-disabled_tests.patch

* Mon May 04 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.81-1.rs
- Latest sources from upstream.
- Updating Source2: mysql.logrotate resolves tracker [#1272] (again)
- Removed Patch218: mysql-5.0.75-openssl.patch (applied upstream)
- Removed Patch219: mysql-5.0.75-bug42037.patch (applied upstream)
- Removed Patch220: mysql-5.0.77-name_const.patch (applied upstream)

* Thu Apr 30 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.77-2.1.rs
- Added Rackspace comment and version suffix
- Updated Source2: mysql.logrorate resolves tracker [#1272]

* Mon Apr 13 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.77-2.rs
- Added Patch220: mysql-5.0.77-name_const.patch. Resolves MySQL Bugs
  #42014, #42553. Resolves Rackspace Tracker [#1206].
- Conflicts: psa < 8.1 ... Resolves Rackspace Tracker [#1225]. 

* Tue Feb 17 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.77-1.rs
- Latest sources from upstream.

* Tue Feb 03 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.75-3.rs
- Adding Patch219: mysql-5.0.75-bug42037.patch 
- lograte changes: No rotations of the mysql error log (this is fundamentally
  broken anyway).  dropped notifempty (logrotate even if the slowquery log
  is empty=failed last rotation).  changed compress to delaycompress (delay
  compres  sing an open file, hopefully flush wont' fail twice in a row).
  changed last-action to postrotate (to attempt flush before any compressing).
  Resolves Rackspace Tracker [#1121].

* Tue Jan 27 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.75-2.rs
- Adding Patch217: mysql-5.0.75-automake_el3.patch. Resolves MySQL
  Bug #42393.
- Adding Patch218: mysql-5.0.75-openssl.patch.  Resolves MySQL 
  Bugs #42366, and #42428.

* Mon Jan 05 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.0.75-1.rs
- Latest sources from upstream.

* Thu Aug 21 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.0.67-2.1.rs
- Added Patch209: mysql-5.0.67-bindir.patch.
- Installing old Redhat init.d/mysqld as default again, and installing
  mysql's init script as /etc/init.d/mysqld-lsb (for upward compatibility).

* Wed Aug 20 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.0.67-2.rs
- Added Patch207: mysql-5.0.67-mysqld_safe.patch 

* Tue Aug 19 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.0.67-1.rs
- Latest sources from upstream
- Use init script from MySQL sources rather than non-lsb compliant Redhat
  version.  Still install old version to init.d/mysqld-redhat (if its preferred).
  This Resolves RS Bug [#265] [MySQL] Remove -R from startup script.
  Also Resolves RS Bug [#282] Rewrite/Maintain LSB-compliant MySQL initscript.
- Added -felide-constructors to CXXFLAGS
- BuildRequires/Requires: libpcap (el5)
- Updated to latest Rackspace my.cnf.
- Recommend passing '-t /tmp' to mysql_upgrade in pre script.
- BuildRequires: gcc
- Modified mysql.logrotate to use --defaults=/root/.my.cnf.  Resolves
  RS Bug [#632] [MySQL 5.x] Rotation of the slow query log is empty.
- Removed Patch211: mysql-5.0.45-log-bin.patch (applied upstream as of 5.0.54).
- Removed Patch12: mysql-5.0.51-CVE-2007-5925.patch (applied upstream).
- Removed Patch212: mysql-5.0.51-openssl-connect.patch (applied upstream).
- Removed Patch215: mysql-5.0.51-disabled-tests.patch (applied upstream).
- Removed Patch216: mysql-5.0.51a-order-by.patch (applied upstream).
- Cluster packages require mysql-server (Resolves Rackspace 
  Bug #[#292] [MySQL] All SubPackages need to Require mysql-server.
- Resolves RS Tracker [#716] [MySQL] 5.0.67 Available.

* Mon Feb 04 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.0.51a-2.rs
- Adding Patch216: mysql-5.0.51a-order-by Patch resolves MySQL Bug #32202
  as well as Rackspace Bug [#291].

* Tue Jan 29 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.0.51a-1.rs
- Latest sources from upstream 
- Removed Patch213: mysql-5.0.51-mysqlcheck.patch (applied upstream)

* Mon Jan 21 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.0.51-1.1.rs
- Only require mysqlclientXX on el3/el4.

* Thu Jan 03 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.0.51-1.rs
- Latest sources from upstream.
- Adding clustering to be more in line with MySQL packages: clusterstorage
  clustermanagement, clustertools, clusterextra.
- Adding Patch212: mysql-5.0.51-openssl-connect.patch (Resolves Bug #33050)
- Adding Patch213: mysql-5.0.51-mysqlcheck.patch (Resolves Bug #26976)
- Adding Patch215: mysql-5.0.51-disabled-tests.patch
- Removing Patch210: mysql-5.0.45-bug29898.patch (applied upstream)
- Removing Patch13: mysql-5.0.45-CVE-2007-5969.patch (applied upstream)
- Removing Patch209: mysql-5.0.45-disabled-tests.patch
- New file %{_datadir}/mysql/mysqld_multi.server

* Fri Dec 21 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.45-4.rs
- Adding Patch12: mysql-5.0.51-CVE-2007-5925.patch
- Adding Patch13: mysql-5.0.45-CVE-2007-5969.patch
- Removed old_passwords hack from pre/post scripts

* Mon Nov 05 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.45-3.5.rs
- pre/post scripts to properly setup ld.so.conf on rhel3
- file checks in pre/post scripts resolves Bug [#244]

* Thu Nov 01 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.45-3.4.rs
- Provides mysqlclient15

* Mon Oct 29 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.45-3.3.rs
- Obsoletes mysqlclient15
- Adding Patch211: mysql-5.0.45-log-bin.patch (resolves MySQL bugs
  28603 and 28597).  Resolves Rackspace Bug [#84] (Invalid default 
  location for log-bin).

* Wed Oct 24 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.45-3.2.rs
- Added my-psa.cnf (Rackspace configuration for Plesk box) 
- Adding /var/lib/mysqllogs for specific logging (bin-log, etc)
- Modified /etc/logrotate.d/mysqld to include slow-log in /var/lib/mysqllogs
- Adding a condition check for el3, and if so use stock my.cnf.  Else, use Rackspace
  configured cnf.
- Added a pre/post hack to set old_passwords=1 if previous config had it.
  This should be removed after this update.  This update changes my.cnf on 
  el4 ... if md5sum has not changed with current config this update will
  bork it (even if it is noreplace) without the pre/post hack.

* Fri Oct 19 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.45-3.rs
- Adding Patch210: mysql-5.0.45-bug29898.patch 
- Recommend running mysql_upgrade, instead of mysql_fix_priviledge_tables.

* Wed Sep 26 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.45-2.rs
- Add -fPIC for all builds (Resolved in MySQL Bug: #18091 and #19999)

* Thu Jul 12 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.45-1.rs
- Latest sources from upstream.
- Making spec 'Mock' compatible.
- Replaced Patch208: mysql-5.0.41-disabled-test.patch with 
  Patch209: mysql-5.0.45-disabled-tests.patch

* Thu May 10 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.41-1.rs
- Latest sources
- Removing Patch206: mysql-5.0.37-disabled-tests.patch 
- The mysql_create_system_tables script was removed from files list
  because mysql_install_db no longer uses it in MySQL 5.0
- Fixing files list for Rhel3 (libz.so.* no longer builds?)
- Removing file listing for usr/share/man/man1/ndb*.gz
- Added Patch208: mysql-5.0.41-disabled-test.patch

* Wed Mar 14 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.37-1.2.rs
- Added a pre script to check version of MySQL, and remind the installer
  to run mysql_fix_privilege_tables if doing a major version upgrade

* Tue Mar 13 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.37-1.1.rs
- Add a hack to allow AS_HELP_STRING in aclocal.m4 (fix for Rhel3 builds)
- Removed mysqlmanager.1.gz from files list

* Mon Mar 12 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.37-1.rs
- Upping to latest sources
- Replacing Patch3: mysql-libtool.patch with Patch303: mysql-5.0.33-libtool.patch
- Replacing Patch204: mysql-5.0.27-testing.patch with Patch304: mysql-5.0.37-testing.patch
- Removing Patch300: mysql-5.0.27-disable-tests.patch
- Removing Patch302: mysql-5.0.27-view-test.patch
- Obsoletes: MySQL, MySQL-server, MySQL-devel
- Adding Patch206: mysql-5.0.37-disabled-tests.patch 
  Bug#27035, Bug#26600 (type error)
  Bug#27061 ssl_des test case fails (timeout)

* Wed Jan 31 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.27-1.rs
- Rebuild with latest sources
- Added Patch300: mysql-5.0.27-disable-tests.patch 
- Added Patch302: mysql-5.0.27-view-test.patch (Bug #25359)
- Replaced Patch1: mysql-libdir.patch with Patch201: mysql-5.0.27-libdir.patch
- Replaced Patch4: mysql-testing.patch with Patch204: mysql-5.0.27-testing.patch 
  New patch Removes '--with-openssl' from mysql tests since MySQL tests against yaSSL 
  and the openssl_1 test fails otherwise (Bug #25988)
- Replaced Patch5: mysql-no-atomic.patch with Patch205: mysql-5.0.27-no-atomic.patch

* Mon Jan 29 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.18-2.3.rs
- Add conditional BuildRequires: gettext for Rhel3 (no -devel there)

* Wed Jan 24 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.0.18-2.2.rs
- Rebuild
- Added os_ver_tag options
- Add Requires mysqlclient10, mysqlclient14 (Rhel3/Rhel4 savvy)
- Added workaround to copy over system mkinstalldirs 
- Added CFLAG condition check for rhel3 (-fwrapv breaks build)
- BuildRequires: gettext-devel
- Condition to list the following on Rhel3 only:
  	- %{_libdir}/mysql/libz.la 
  	- %{_libdir}/mysql/libz.so.1.2.3

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.0.18-2.1
- bump again for double-long bug on ppc(64)

* Thu Feb  9 2006 Tom Lane <tgl@redhat.com> 5.0.18-2
- err-log option has been renamed to log-error, fix my.cnf and initscript

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.0.18-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan  5 2006 Tom Lane <tgl@redhat.com> 5.0.18-1
- Update to MySQL 5.0.18

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 5.0.16-4
- fix my_config.h for ppc platforms

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 5.0.16-3
- my_config.h needs to guard against 64-bit platforms that also define the
  32-bit symbol

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 5.0.16-2
- oops, looks like we want uname -i not uname -m

* Mon Dec 12 2005 Tom Lane <tgl@redhat.com> 5.0.16-1
- Update to MySQL 5.0.16
- Add EXCEPTIONS-CLIENT license info to the shipped documentation
- Make my_config.h architecture-independent for multilib installs;
  put the original my_config.h into my_config_$ARCH.h
- Add -fwrapv to CFLAGS so that gcc 4.1 doesn't break it

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Tom Lane <tgl@redhat.com> 5.0.15-3
- Make stop script wait for daemon process to disappear (bz#172426)

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 5.0.15-2
- Rebuild due to openssl library update.

* Thu Nov  3 2005 Tom Lane <tgl@redhat.com> 5.0.15-1
- Update to MySQL 5.0.15 (scratch build for now)

* Wed Oct  5 2005 Tom Lane <tgl@redhat.com> 4.1.14-1
- Update to MySQL 4.1.14

* Tue Aug 23 2005 Tom Lane <tgl@redhat.com> 4.1.12-3
- Use politically correct patch name.

* Tue Jul 12 2005 Tom Lane <tgl@redhat.com> 4.1.12-2
- Fix buffer overflow newly exposed in isam code; it's the same issue
  previously found in myisam, and not very exciting, but I'm tired of
  seeing build warnings.

* Mon Jul 11 2005 Tom Lane <tgl@redhat.com> 4.1.12-1
- Update to MySQL 4.1.12 (includes a fix for bz#158688, bz#158689)
- Extend mysql-test-ssl.patch to solve rpl_openssl test failure (bz#155850)
- Update mysql-lock-ssl.patch to match the upstream committed version
- Add --with-isam to re-enable the old ISAM table type, per bz#159262
- Add dependency on openssl-devel per bz#159569
- Remove manual.txt, as upstream decided not to ship it anymore;
  it was redundant with the mysql.info file anyway.

* Mon May  9 2005 Tom Lane <tgl@redhat.com> 4.1.11-4
- Include proper locking for OpenSSL in the server, per bz#155850

* Mon Apr 25 2005 Tom Lane <tgl@redhat.com> 4.1.11-3
- Enable openssl tests during build, per bz#155850
- Might as well turn on --disable-dependency-tracking

* Fri Apr  8 2005 Tom Lane <tgl@redhat.com> 4.1.11-2
- Avoid dependency on <asm/atomic.h>, cause it won't build anymore on ia64.
  This is probably a cleaner solution for bz#143537, too.

* Thu Apr  7 2005 Tom Lane <tgl@redhat.com> 4.1.11-1
- Update to MySQL 4.1.11 to fix bz#152911 as well as other issues
- Move perl-DBI, perl-DBD-MySQL dependencies to server package (bz#154123)
- Override configure thread library test to suppress HAVE_LINUXTHREADS check
- Fix BDB failure on s390x (bz#143537)
- At last we can enable "make test" on all arches

* Fri Mar 11 2005 Tom Lane <tgl@redhat.com> 4.1.10a-1
- Update to MySQL 4.1.10a to fix security vulnerabilities (bz#150868,
  for CAN-2005-0711, and bz#150871 for CAN-2005-0709, CAN-2005-0710).

* Sun Mar  6 2005 Tom Lane <tgl@redhat.com> 4.1.10-3
- Fix package Requires: interdependencies.

* Sat Mar  5 2005 Tom Lane <tgl@redhat.com> 4.1.10-2
- Need -fno-strict-aliasing in at least one place, probably more.
- Work around some C spec violations in mysql.

* Fri Feb 18 2005 Tom Lane <tgl@redhat.com> 4.1.10-1
- Update to MySQL 4.1.10.

* Sat Jan 15 2005 Tom Lane <tgl@redhat.com> 4.1.9-1
- Update to MySQL 4.1.9.

* Wed Jan 12 2005 Tom Lane <tgl@redhat.com> 4.1.7-10
- Don't assume /etc/my.cnf will specify pid-file (bz#143724)

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 4.1.7-9
- Rebuilt for new readline.

* Tue Dec 21 2004 Tom Lane <tgl@redhat.com> 4.1.7-8
- Run make test on all archs except s390x (which seems to have a bdb issue)

* Mon Dec 13 2004 Tom Lane <tgl@redhat.com> 4.1.7-7
- Suppress someone's silly idea that libtool overhead can be skipped

* Sun Dec 12 2004 Tom Lane <tgl@redhat.com> 4.1.7-6
- Fix init script to not need a valid username for startup check (bz#142328)
- Fix init script to honor settings appearing in /etc/my.cnf (bz#76051)
- Enable SSL (bz#142032)

* Thu Dec  2 2004 Tom Lane <tgl@redhat.com> 4.1.7-5
- Add a restorecon to keep the mysql.log file in the right context (bz#143887)

* Tue Nov 23 2004 Tom Lane <tgl@redhat.com> 4.1.7-4
- Turn off old_passwords in default /etc/my.cnf file, for better compatibility
  with mysql 3.x clients (per suggestion from Joe Orton).

* Fri Oct 29 2004 Tom Lane <tgl@redhat.com> 4.1.7-3
- Handle ldconfig more cleanly (put a file in /etc/ld.so.conf.d/).

* Thu Oct 28 2004 Tom Lane <tgl@redhat.com> 4.1.7-2
- rebuild in devel branch

* Wed Oct 27 2004 Tom Lane <tgl@redhat.com> 4.1.7-1
- Update to MySQL 4.1.x.

* Tue Oct 12 2004 Tom Lane <tgl@redhat.com> 3.23.58-13
- fix security issues CAN-2004-0835, CAN-2004-0836, CAN-2004-0837
  (bugs #135372, 135375, 135387)
- fix privilege escalation on GRANT ALL ON `Foo\_Bar` (CAN-2004-0957)

* Wed Oct 06 2004 Tom Lane <tgl@redhat.com> 3.23.58-12
- fix multilib problem with mysqlbug and mysql_config
- adjust chkconfig priority per bug #128852
- remove bogus quoting per bug #129409 (MySQL 4.0 has done likewise)
- add sleep to mysql.init restart(); may or may not fix bug #133993

* Tue Oct 05 2004 Tom Lane <tgl@redhat.com> 3.23.58-11
- fix low-priority security issues CAN-2004-0388, CAN-2004-0381, CAN-2004-0457
  (bugs #119442, 125991, 130347, 130348)
- fix bug with dropping databases under recent kernels (bug #124352)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 3.23.58-10
- rebuilt

* Sat Apr 17 2004 Warren Togami <wtogami@redhat.com> 3.23.58-9
- remove redundant INSTALL-SOURCE, manual.*
- compress manual.txt.bz2
- BR time

* Tue Mar 16 2004 Tom Lane <tgl@redhat.com> 3.23.58-8
- repair logfile attributes in %%files, per bug #102190
- repair quoting problem in mysqlhotcopy, per bug #112693
- repair missing flush in mysql_setpermission, per bug #113960
- repair broken error message printf, per bug #115165
- delete mysql user during uninstall, per bug #117017
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Tom Lane <tgl@redhat.com>
- fix chown syntax in mysql.init
- rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Nov 18 2003 Kim Ho <kho@redhat.com> 3.23.58-5
- update mysql.init to use anonymous user (UNKNOWN_MYSQL_USER) for
  pinging mysql server (#108779)

* Mon Oct 27 2003 Kim Ho <kho@redhat.com> 3.23.58-4
- update mysql.init to wait (max 10 seconds) for mysql server to 
  start (#58732)

* Mon Oct 27 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.58-3
- re-enable Berkeley DB support (#106832)
- re-enable ia64 testing

* Fri Sep 19 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.58-2
- rebuilt

* Mon Sep 15 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.58-1
- upgrade to 3.23.58 for security fix

* Tue Aug 26 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.57-2
- rebuilt

* Wed Jul 02 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.57-1
- revert to prior version of MySQL due to license incompatibilities 
  with packages that link against the client.  The MySQL folks are
  looking into the issue.

* Wed Jun 18 2003 Patrick Macdonald <patrickm@redhat.com> 4.0.13-4
- restrict test on ia64 (temporary)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 4.0.13-3
- rebuilt

* Thu May 29 2003 Patrick Macdonald <patrickm@redhat.com> 4.0.13-2
- fix filter-requires-mysql.sh with less restrictive for mysql-bench 

* Wed May 28 2003 Patrick Macdonald <patrickm@redhat.com> 4.0.13-1
- update for MySQL 4.0
- back-level shared libraries available in mysqlclient10 package

* Fri May 09 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.56-2
- add sql-bench package (#90110) 

* Wed Mar 19 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.56-1
- upgrade to 3.23.56 for security fixes
- remove patch for double-free (included in 3.23.56) 

* Tue Feb 18 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.54a-11
- enable thread safe client
- add patch for double free fix

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Karsten Hopp <karsten@redhat.de> 3.23.54a-9
- disable checks on s390x

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 3.23.54a-8
- use internal dep generator.

* Wed Jan  1 2003 Bill Nottingham <notting@redhat.com> 3.23.54a-7
- fix mysql_config on hammer

* Sun Dec 22 2002 Tim Powers <timp@redhat.com> 3.23.54a-6
- don't use rpms internal dep generator

* Tue Dec 17 2002 Elliot Lee <sopwith@redhat.com> 3.23.54a-5
- Push it into the build system

* Mon Dec 16 2002 Joe Orton <jorton@redhat.com> 3.23.54a-4
- upgrade to 3.23.54a for safe_mysqld fix

* Thu Dec 12 2002 Joe Orton <jorton@redhat.com> 3.23.54-3
- upgrade to 3.23.54 for latest security fixes

* Tue Nov 19 2002 Jakub Jelinek <jakub@redhat.com> 3.23.52-5
- Always include <errno.h> for errno
- Remove unpackaged files

* Tue Nov 12 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not prereq userdel, not used at all

* Mon Sep  9 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.52-4
- Use %%{_libdir}
- Add patch for x86-64

* Wed Sep  4 2002 Jakub Jelinek <jakub@redhat.com> 3.23.52-3
- rebuilt with gcc-3.2-7

* Thu Aug 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.52-2
- Add --enable-local-infile to configure - a new option
  which doesn't default to the old behaviour (#72885)

* Fri Aug 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.52-1
- 3.23.52. Fixes a minor security problem, various bugfixes.

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com> 3.23.51-5
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.51-4
- rebuild

* Thu Jul 18 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.51-3
- Fix #63543 and #63542 

* Thu Jul 11 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.51-2
- Turn off bdb on PPC(#68591)
- Turn off the assembly optimizations, for safety. 

* Wed Jun 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.51-1
- Work around annoying auto* thinking this is a crosscompile
- 3.23.51

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 10 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.50-2
- Add dependency on perl-DBI and perl-DBD-MySQL (#66349)

* Thu May 30 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.50-1
- 3.23.50

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.49-4
- Rebuild
- Don't set CXX to gcc, it doesn't work anymore
- Exclude Alpha

* Mon Apr  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.49-3
- Add the various .cnf examples as doc files to mysql-server (#60349)
- Don't include manual.ps, it's just 200 bytes with a URL inside (#60349)
- Don't include random files in /usr/share/mysql (#60349)
- langify (#60349)

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.49-2
- Rebuild

* Sun Feb 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.49-1
- 3.23.49

* Thu Feb 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.48-2
- work around perl dependency bug.

* Mon Feb 11 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.48-1
- 3.23.48

* Thu Jan 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.47-4
- Use kill, not mysqladmin, to flush logs and shut down. Thus, 
  an admin password can be set with no problems.
- Remove reload from init script

* Wed Jan 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.47-3
- remove db3-devel from buildrequires, 
  MySQL has had its own bundled copy since the mid thirties

* Sun Jan  6 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.23.47-1
- 3.23.47
- Don't build for alpha, toolchain immature.

* Mon Dec  3 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.23.46-1
- 3.23.46
- use -fno-rtti and -fno-exceptions, and set CXX to increase stability. 
  Recommended by mysql developers.

* Sun Nov 25 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.23.45-1
- 3.23.45

* Wed Nov 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.23.44-2
- centralize definition of datadir in the initscript (#55873)

* Fri Nov  2 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.23.44-1
- 3.23.44

* Thu Oct  4 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.23.43-1
- 3.23.43

* Mon Sep 10 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.23.42-1
- 3.23.42
- reenable innodb

* Tue Aug 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.23.41-1
- 3.23.41 bugfix release
- disable innodb, to avoid the broken updates
- Use "mysqladmin flush_logs" instead of kill -HUP in logrotate 
  script (#51711)

* Sat Jul 21 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.40, bugfix release
- Add zlib-devel to buildrequires:

* Fri Jul 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- BuildRequires-tweaking

* Thu Jun 28 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Reenable test, but don't run them for s390, s390x or ia64
- Make /etc/my.cnf config(noplace). Same for /etc/logrotate.d/mysqld

* Thu Jun 14 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.29
- enable innodb
- enable assembly again
- disable tests for now...

* Tue May 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.38
- Don't use BDB on Alpha - no fast mutexes

* Tue Apr 24 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.37
- Add _GNU_SOURCE to the compile flags

* Wed Mar 28 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Make it obsolete our 6.2 PowerTools packages
- 3.23.36 bugfix release - fixes some security issues
  which didn't apply to our standard configuration
- Make "make test" part of the build process, except on IA64
  (it fails there)

* Tue Mar 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.35 bugfix release
- Don't delete the mysql user on uninstall

* Tue Mar 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.34a bugfix release

* Wed Feb  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- added readline-devel to BuildRequires:

* Tue Feb  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- small i18n-fixes to initscript (action needs $)

* Tue Jan 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- make it shut down and rotate logs without using mysqladmin 
  (from #24909)

* Mon Jan 29 2001 Trond Eivind Glomsrød <teg@redhat.com>
- conflict with "MySQL"

* Tue Jan 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- improve gettextizing

* Mon Jan 22 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.32
- fix logrotate script (#24589)

* Wed Jan 17 2001 Trond Eivind Glomsrød <teg@redhat.com>
- gettextize
- move the items in Requires(post): to Requires: in preparation
  for an errata for 7.0 when 3.23.31 is released
- 3.23.31

* Tue Jan 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- add the log file to the rpm database, and make it 0640
  (#24116)
- as above in logrotate script
- changes to the init sequence - put most of the data
  in /etc/my.cnf instead of hardcoding in the init script
- use /var/run/mysqld/mysqld.pid instead of 
  /var/run/mysqld/pid
- use standard safe_mysqld
- shut down cleaner

* Mon Jan 08 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.30
- do an explicit chmod on /var/lib/mysql in post, to avoid 
  any problems with broken permissons. There is a report
  of rm not changing this on its own (#22989)

* Mon Jan 01 2001 Trond Eivind Glomsrød <teg@redhat.com>
- bzipped source
- changed from 85 to 78 in startup, so it starts before
  apache (which can use modules requiring mysql)

* Wed Dec 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.29a

* Tue Dec 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add requirement for new libstdc++, build for errata

* Mon Dec 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.29

* Mon Nov 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.28 (gamma)
- remove old patches, as they are now upstreamed

* Thu Nov 14 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Add a requirement for a new glibc (#20735)
- build on IA64

* Wed Nov  1 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable more assembly

* Wed Nov  1 2000 Jakub Jelinek <jakub@redhat.com>
- fix mysql on SPARC (#20124)

* Tue Oct 31 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.27

* Wed Oct 25 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add patch for fixing bogus aliasing in mysql from Jakub,
  which should fix #18905 and #18620

* Mon Oct 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- check for negative niceness values, and negate it
  if present (#17899)
- redefine optflags on IA32 FTTB

* Wed Oct 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.26, which among other fixes now uses mkstemp()
  instead of tempnam().
- revert changes made yesterday, the problem is now
  isolated
 
* Tue Oct 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use the compat C++ compiler FTTB. Argh.
- add requirement of ncurses4 (see above)

* Sun Oct 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.25
- fix shutdown problem (#17956)

* Tue Sep 26 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Don't try to include no-longer-existing PUBLIC file
  as doc (#17532)

* Thu Sep 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rename config file to /etc/my.cnf, which is what
  mysqld wants... doh. (#17432)
- include a changed safe_mysqld, so the pid file option
  works. 
- make mysql dir world readable to they can access the 
  mysql socket. (#17432)
- 3.23.24

* Wed Sep 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.23

* Sun Aug 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Add "|| :" to condrestart to avoid non-zero exit code

* Thu Aug 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- it's mysql.com, not mysql.org and use correct path to 
  source (#16830)

* Wed Aug 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- source file from /etc/rc.d, not /etc/rd.d. Doh.

* Sun Aug 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't run ldconfig -n, it doesn't update ld.so.cache
  (#16034)
- include some missing binaries
- use safe_mysqld to start the server (request from
  mysql developers)

* Sat Aug 05 2000 Bill Nottingham <notting@redhat.com>
- condrestart fixes

* Mon Aug 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.22. Disable the old patches, they're now in.

* Thu Jul 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- bugfixes in the initscript
- move the .so link to the devel package

* Wed Jul 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild due to glibc changes

* Tue Jul 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable compiler patch
- don't include info directory file

* Mon Jul 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- move back to /etc/rc.d/init.d

* Fri Jul 14 2000 Trond Eivind Glomsrød <teg@redhat.com>
- more cleanups in initscript

* Thu Jul 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add a patch to work around compiler bug 
  (from monty@mysql.com) 

* Wed Jul 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't build the SQL daemon statically (glibc problems)
- fix the logrotate script - only flush log if mysql
  is running
- change the reloading procedure 
- remove icon - glint is obsolete a long time ago

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- try the new compiler again
- build the SQL daemon statically
- add compile time support for complex charsets
- enable assembler
- more cleanups in initscript

* Sun Jul 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use old C++ compiler
- Exclusivearch x86

* Sat Jul 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- move .so files to devel package
- more cleanups
- exclude sparc for now

* Wed Jul 05 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.23.21
- remove file from /etc/sysconfig
- Fix initscript a bit - initialization of databases doesn't
  work yet
- specify the correct licenses
- include a /etc/my.conf (empty, FTTB)
- add conditional restart to spec file

* Tue Jul  2 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- update to 3.23.20
- use %%configure, %%makeinstall, %%{_tmppath}, %%{_mandir},
  %%{_infodir}, /etc/init.d
- remove the bench package
- change some of the descriptions a little bit
- fix the init script
- some compile fixes
- specify mysql user
- use mysql uid 27 (postgresql is 26)
- don't build on ia64

* Sat Feb 26 2000 Jos Vos <jos@xos.nl>
- Version 3.22.32 release XOS.1 for LinuX/OS 1.8.0
- Upgrade from version 3.22.27 to 3.22.32.
- Do "make install" instead of "make install-strip", because "install -s"
  now appears to fail on various scripts.  Afterwards, strip manually.
- Reorganize subpackages, according to common Red Hat packages: the client
  program and shared library become the base package and the server and
  some accompanying files are now in a separate server package.  The
  server package implicitly requires the base package (shared library),
  but we have added a manual require tag anyway (because of the shared
  config file, and more).
- Rename the mysql-benchmark subpackage to mysql-bench.

* Mon Jan 31 2000 Jos Vos <jos@xos.nl>
- Version 3.22.27 release XOS.2 for LinuX/OS 1.7.1
- Add post(un)install scripts for updating ld.so.conf (client subpackage).

* Sun Nov 21 1999 Jos Vos <jos@xos.nl>
- Version 3.22.27 release XOS.1 for LinuX/OS 1.7.0
- Initial version.
- Some ideas borrowed from Red Hat Powertools 6.1, although this spec
  file is a full rewrite from scratch.
