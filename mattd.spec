%global modname mattd.core

Name:           mattd
Version:        0.0.1
Release:        1%{?dist}
Summary:        Voice-to-text scripting engine.  Matt Daemon.
Group:          Applications/Internet
License:        AGPLv3+
URL:            http://mattd.rtfd.org/
Source0:        http://pypi.python.org/packages/source/m/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-daemon

Requires:       pocketsphinx-plugin
Requires:       pygtk2

%description
Matt Daemon is a voice-to-text-to-plugin service.  Write plugins to carry out
your every whim!

%prep
%setup -q -n %{modname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

%{__mkdir_p} %{buildroot}%{_sysconfdir}/mattd.d/
%{__cp} mattd.d/main.ini %{buildroot}%{_sysconfdir}/mattd.d/.

%{__mkdir_p} %{buildroot}/%{_var}/run/%{modname}
%{__mkdir_p} %{buildroot}/%{_var}/log/%{modname}

%{__mkdir_p} %{buildroot}%{_sysconfdir}/init.d
%{__install} init.d/mattd.init %{buildroot}%{_sysconfdir}/init.d/mattd

cp %{_bindir}/mattd %{_sbindir}/mattd

%pre
%{_sbindir}/groupadd -r mattd &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d %{_datadir}/mattd -M \
                     -c 'Matt Daemon' -g mattd mattd &>/dev/null || :

%post
/sbin/chkconfig --add mattd

%preun
if [ $1 -eq 0 ]; then
    /sbin/service mattd stop >/dev/null 2>&1
    /sbin/chkconfig --del mattd
fi

%files
%doc README.rst LICENSE
%attr(755, %{modname}, %{modname}) %dir %{_var}/log/%{modname}
%attr(755, %{modname}, %{modname}) %dir %{_var}/run/%{modname}

%{python_sitelib}/%{modname}/
%{python_sitelib}/%{modname}-%{version}-py*.egg-info/

%config(noreplace) %{_sysconfdir}/mattd.d

%{_sbindir}/mattd
%{_sysconfdir}/init.d/mattd

%changelog
* Fri Aug 24 2012 Ralph Bean <rbean@redhat.com> - 0.0.1-1
- Initial packaging.
