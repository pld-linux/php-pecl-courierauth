%define		php_name	php%{?php_suffix}
%define		modname	courierauth
%define		status		beta
Summary:	%{modname} - binding to courier-authlib library
Summary(pl.UTF-8):	%{modname} - wiązanie do biblioteki courier-authlib
Name:		%{php_name}-pecl-%{modname}
Version:	0.1.0
Release:	2
License:	BSD, revised
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	b7411d4fa8f297166bf5742d3d7c3df5
URL:		http://pecl.php.net/package/courierauth/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	courier-authlib-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Provides means for authentication against any courier authdaemond
backends.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Pakiet ten udostępnia możliwość uwierzytelniania względem dowolnego
backendu authdaemond couriera.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
