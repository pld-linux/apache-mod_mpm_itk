%define		mod_name	mpm_itk
%define		apxs		/usr/sbin/apxs
%define		ver	2.4.7
%define		subver	01
Summary:	mod_mpm_itk - allows you to run each of your vhost under a separate uid and gid
Name:		apache-mod_mpm_itk
Version:	%{ver}.%{subver}
Release:	1
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	http://mpm-itk.sesse.net/mpm-itk-%{ver}-%{subver}.tar.gz
# Source0-md5:	3d7a14aef93bb5c1eb1c01081585c4bc
URL:		http://mpm-itk.sesse.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.4.7
BuildRequires:	apr-devel >= 1:1.0
BuildRequires:	apr-util-devel >= 1:1.0
BuildRequires:	libcap-devel
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	apache-base >= 2.4.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
apache2-mpm-itk (just mpm-itk for short) is an MPM (Multi-Processing
Module) for the Apache web server. mpm-itk allows you to run each of
your vhost under a separate uid and gid—in short, the scripts and
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

install .libs/mpm_itk.so $RPM_BUILD_ROOT%{_pkglibdir}

echo "LoadModule mpm_itk_module	modules/mod_mpm_itk.so" > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/10_mod_%{mod_name}.conf

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
%attr(755,root,root) %{_pkglibdir}/mpm_itk.so
