%global modname mattd.core

Name:           mattd
Version:        0.0.5
Release:        4%{?dist}
Summary:        Voice-to-text scripting engine.  Matt Daemon.
Group:          Applications/Internet
License:        AGPLv3+
URL:            http://mattd.rtfd.org/
Source0:        http://pypi.python.org/packages/source/m/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-daemon

Requires:       python-daemon
Requires:       pocketsphinx-plugin
Requires:       gstreamer-python
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

%{__mkdir_p} %{buildroot}/%{_datadir}/mattd

%{__mkdir_p} %{buildroot}/%{_var}/run/mattd
%{__mkdir_p} %{buildroot}/%{_var}/log/mattd

%{__mkdir_p} %{buildroot}%{_sysconfdir}/init.d
%{__install} init.d/mattd.init %{buildroot}%{_sysconfdir}/init.d/mattd

%{__mkdir_p} %{buildroot}/%{_sbindir}
mv %{buildroot}/%{_bindir}/mattd %{buildroot}/%{_sbindir}/mattd

%{__mkdir_p} %{buildroot}%{_sysconfdir}/mattd.d/
cp production.ini %{buildroot}%{_sysconfdir}/mattd.d/main.ini

%pre
bash
#%{_sbindir}/groupadd -r mattd || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d %{_datadir}/mattd -M \
                     -c 'Matt Daemon' mattd || :

%post
/sbin/chkconfig --add mattd

%preun
if [ $1 -eq 0 ]; then
    /sbin/service mattd stop >/dev/null 2>&1
    /sbin/chkconfig --del mattd
fi

%files
%doc README.rst LICENSE
%attr(755, mattd, mattd) %dir %{_var}/log/mattd
%attr(755, mattd, mattd) %dir %{_var}/run/mattd
%attr(755, mattd, mattd) %dir %{_datadir}/mattd
%config(noreplace) %{_sysconfdir}/mattd.d
%{_sysconfdir}/init.d/mattd
%{_sbindir}/mattd

%{python_sitelib}/mattd/
%{python_sitelib}/%{modname}-%{version}-py*.egg-info/
%{python_sitelib}/%{modname}-%{version}-py*.pth


%changelog
* Mon Aug 27 2012 Ralph Bean <rbean@redhat.com> - 0.0.5-4
- Include production.ini.
- Fixes to groupadd and useradd in %%pre

* Mon Aug 27 2012 Ralph Bean <rbean@redhat.com> - 0.0.4-1
- Forgotten items in the tarball and BuildRequires.

* Mon Aug 27 2012 Ralph Bean <rbean@redhat.com> - 0.0.3-1
- New, more stable upstream version.

* Fri Aug 24 2012 Ralph Bean <rbean@redhat.com> - 0.0.1-1
- Initial packaging.
