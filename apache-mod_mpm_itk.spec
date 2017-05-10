%define		mod_name	mpm_itk
%define		apxs		/usr/sbin/apxs
%define		ver	2.4.7
%define		subver	04
Summary:	mod_mpm_itk - allows you to run each of your vhost under a separate uid and gid
Name:		apache-mod_mpm_itk
Version:	%{ver}.%{subver}
Release:	2
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	http://mpm-itk.sesse.net/mpm-itk-%{ver}-%{subver}.tar.gz
# Source0-md5:	a25d8db440858b593f1d6a4938fa3d02
Source1:	%{name}.conf
Source2:	%{name}-php.conf
Source3:	%{name}.tmpfiles
URL:		http://mpm-itk.sesse.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.4.7
BuildRequires:	apr-devel >= 1:1.0
BuildRequires:	apr-util-devel >= 1:1.0
BuildRequires:	libcap-devel
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	apache-base >= 2.4.7
Requires:	php-dirs >= 1.5-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
apache2-mpm-itk (just mpm-itk for short) is an MPM (Multi-Processing
Module) for the Apache web server. mpm-itk allows you to run each of
your vhost under a separate uid and gid - in short, the scripts and
configuration files for one vhost no longer have to be readable for
all the other vhosts.

mpm-itk is based on the traditional prefork MPM, which means it's
non-threaded; in short, this means you can run non-thread-aware code
(like many PHP extensions) without problems. On the other hand, you
lose out to any performance benefit you'd get with threads, of course;
you'd have to decide for yourself if that's worth it or not. You will
also take an additional performance hit over prefork, since there's an
extra fork per request.

%prep
%setup -q -n mpm-itk-%{ver}-%{subver}

%build
%configure \
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_pkglibdir},%{_sysconfdir}/conf.d}
install -d $RPM_BUILD_ROOT{/var/run/php-ug,%{systemdtmpfilesdir}}

install -p .libs/mpm_itk.so $RPM_BUILD_ROOT%{_pkglibdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/10_mod_%{mod_name}.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/99_mod_%{mod_name}-php.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/php-itk-dirs.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}-php.conf
%attr(755,root,root) %{_pkglibdir}/mpm_itk.so
%{systemdtmpfilesdir}/php-itk-dirs.conf
# multiple uid/gids in use
%dir %attr(1773,root,root) /var/run/php-ug

