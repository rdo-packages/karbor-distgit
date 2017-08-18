%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 0
%global pypi_name cinder

%if 0%{?rhel} || 0%{?fedora}
%global rdo 1
%endif

Name:           openstack-karbor
Epoch:          1
Version:        XXX
Release:        XXX
Summary:        OpenStack Application Data Protection Service

License:        ASL 2.0
Url:            https://launchpad.net/karbor
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

Source1:        openstack-karbor.logrotate

Source2:        openstack-karbor-operationengine.service
Source3:        openstack-karbor-protection.service


BuildArch:      noarch
BuildRequires:  openstack-macros
BuildRequires:  openstack-tempest
BuildRequires:  python-babel
BuildRequires:  python-paste
BuildRequires:  python-paste-deploy
BuildRequires:  python-routes
BuildRequires:  python-sqlalchemy
BuildRequires:  python-webob
BuildRequires:  python-webtest
BuildRequires:  python-abclient
BuildRequires:  python-bcrypt
BuildRequires:  python-cinderclient
BuildRequires:  python-croniter
BuildRequires:  python-devel
BuildRequires:  python-eventlet
BuildRequires:  python-fixtures
BuildRequires:  python-freezegun
BuildRequires:  python-glanceclient
BuildRequires:  python-greenlet
BuildRequires:  python-heatclient
BuildRequires:  python-icalendar
BuildRequires:  python-karborclient
BuildRequires:  python-keystoneauth1
BuildRequires:  python-keystonemiddleware
BuildRequires:  python-lxml
BuildRequires:  python-manilaclient
BuildRequires:  python-mock
BuildRequires:  python-neutronclient
BuildRequires:  python-novaclient
BuildRequires:  python-os-api-ref
BuildRequires:  python-os-testr
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-context
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-oslo-middleware
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-service
BuildRequires:  python-oslo-versionedobjects
BuildRequires:  python-reno
BuildRequires:  python-requests
BuildRequires:  python-six
BuildRequires:  python-migrate
BuildRequires:  python-stevedore
BuildRequires:  python-swiftclient
BuildRequires:  python-taskflow

Requires:       logrotate
Requires:       python-karbor = %{epoch}:%{version}-%{release}
BuildRequires:  systemd

%description
Karbor is a Python implementation of the OpenStack
(http://www.openstack.org) Application Data Protection API.
.
This package contains the karbor python libraries.

%package -n     python-karbor
Summary:        Karbor Python libraries
Group:          Applications/System
Requires:       python-babel
Requires:       python-paste
Requires:       python-paste-deploy
Requires:       python-routes
Requires:       python-sqlalchemy
Requires:       python-webob
Requires:       python-abclient
Requires:       python-cinderclient
Requires:       python-croniter
Requires:       python-eventlet
Requires:       python-glanceclient
Requires:       python-greenlet
Requires:       python-heatclient
Requires:       python-icalendar
Requires:       python-karborclient
Requires:       python-keystoneauth1
Requires:       python-keystonemiddleware
Requires:       python-manilaclient
Requires:       python-neutronclient
Requires:       python-novaclient
Requires:       python-oslo-concurrency
Requires:       python-oslo-config
Requires:       python-oslo-context
Requires:       python-oslo-db
Requires:       python-oslo-i18n
Requires:       python-oslo-log
Requires:       python-oslo-messaging
Requires:       python-oslo-middleware
Requires:       python-oslo-policy
Requires:       python-oslo-serialization
Requires:       python-oslo-service
Requires:       python-oslo-versionedobjects
Requires:       python-requests
Requires:       python-six
Requires:       python-migrate
Requires:       python-stevedore
Requires:       python-swiftclient
Requires:       python-taskflow

%description -n   python-karbor
Karbor is a Python implementation of the OpenStack
(http://docs.openstack.org/developer/karbor/) Application Data Protection API.
This package contains the Karbor Python library.

%if 0%{?with_doc}
%package doc
Summary:        Documentation for OpenStack Application Data Protection Service
Group:          Documentation
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
OpenStack Karbor documentaion.
.
This package contains the documentation
%endif

%package api
%define apache_name         httpd
%define apache_site_dir     %{_sysconfdir}/%{apache_name}/conf.d/
BuildRequires:  mod_wsgi
Requires:       mod_wsgi
Summary:        OpenStack Karbor - API service
Group:          Applications/System
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description api
OpenStack Karbor API service.

%package        operationengine
Summary:        OpenStack Karbor OperationEngine service
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    operationengine
OpenStack Karbor OperationEngine service.

%package        protection
Summary:        OpenStack Karbor Protection service
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    protection
OpenStack Karbor Protection service.

%prep
%autosetup -n karbor-%{upstream_version} -S git
%py_req_cleanup


%build
%{py2_build}
export PYTHONPATH="."
# config file generation
oslo-config-generator --config-file etc/oslo-config-generator/karbor.conf \
--output-file etc/karbor.conf.sample
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
%{py2_install}

# Install config files
mkdir -p %{buildroot}%{_sysconfdir}/karbor/
mkdir -p %{buildroot}%{_sysconfdir}/karbor/providers.d/
install -p -D -m 640 etc/karbor.conf.sample %{buildroot}%{_sysconfdir}/karbor/karbor.conf
install -p -D -m 640 etc/api-paste.ini %{buildroot}%{_sysconfdir}/karbor/api-paste.ini
install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/karbor/policy.json
install -p -D -m 640 etc/providers.d/*.conf %{buildroot}%{_sysconfdir}/karbor/providers.d/

# Setup log directory
mkdir -p %{buildroot}%{_localstatedir}/log/karbor

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-karbor

# Install apache configuration files
sed -i 's#/local/bin#/bin#' etc/apache2/apache-karbor-api.conf
%if 0%{?rdo}
# adjust paths to WSGI scripts
sed -i 's#apache2#httpd#' etc/apache2/apache-karbor-api.conf
%endif
install -d -m 755 %{buildroot}%{apache_site_dir}
install -p -D -m 644 etc/apache2/apache-karbor-api.conf  %{buildroot}%{_datarootdir}/karbor/wsgi-karbor.conf
install -p -D -m 644 etc/apache2/apache-karbor-api.conf  %{buildroot}%{apache_site_dir}/karbor.conf

# systemd unitfiles
install -p -D -m 644 %SOURCE2 %{buildroot}%{_unitdir}/openstack-karbor-operationengine.service
install -p -D -m 644 %SOURCE3 %{buildroot}%{_unitdir}/openstack-karbor-protection.service


%pre
%openstack_pre_user_group_create karbor karbor


%post operationengine
%systemd_post openstack-karbor-operationengine.service


%preun operationengine
%systemd_preun openstack-karbor-operationengine.service


%postun operationengine
%systemd_postun_with_restart openstack-karbor-operationengine.service


%post protection
%systemd_post openstack-karbor-protection.service


%preun protection
%systemd_preun openstack-karbor-protection.service


%postun protection
%systemd_postun_with_restart openstack-karbor-protection.service


%files
%license LICENSE
%doc README.rst
%dir %{_datarootdir}/karbor/
%dir %attr(0750, root, karbor) %{_sysconfdir}/karbor/
%dir %attr(0750, root, karbor) %{_sysconfdir}/karbor/providers.d/
%dir %attr(0750, karbor, karbor) %{_localstatedir}/log/karbor
%{_bindir}/karbor-manage
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-karbor
%config(noreplace) %attr(0640, root, karbor) %{_sysconfdir}/karbor/karbor.conf
%config(noreplace) %attr(0640, root, karbor) %{_sysconfdir}/karbor/api-paste.ini
%config(noreplace) %attr(0640, root, karbor) %{_sysconfdir}/karbor/policy.json
%config(noreplace) %attr(0640, root, karbor) %{_sysconfdir}/karbor/providers.d/*.conf

%files -n python-karbor
%license LICENSE
%{python2_sitelib}/karbor/
%{python2_sitelib}/karbor-*.egg-info

%files api
%{_bindir}/karbor-api
%{_bindir}/karbor-wsgi
%{_datarootdir}/karbor/wsgi-karbor.conf
%{apache_site_dir}/karbor.conf

%files operationengine
%{_bindir}/karbor-operationengine
%{_unitdir}/openstack-karbor-operationengine.service

%files protection
%{_bindir}/karbor-protection
%{_unitdir}/openstack-karbor-protection.service

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
