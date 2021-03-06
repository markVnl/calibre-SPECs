 %bcond_without check

%global modname service-identity
%global srcname service_identity

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           python-%{modname}
Version:        16.0.0
Release:        8%{?dist}
Summary:        Service identity verification for pyOpenSSL

License:        MIT
URL:            https://github.com/pyca/service_identity
Source0:        %{url}/archive/%{version}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

%global _description \
Service Identity Verification for pyOpenSSL.\
\
TL;DR: Use this package if you use pyOpenSSL and don’t want to be MITMed.\
\
service_identity aspires to give you all the tools you need for verifying\
whether a certificate is valid for the intended purposes.\
\
In the simplest case, this means host name verification. However,\
service_identity implements RFC 6125 fully and plans to add other\
relevant RFCs too.

%description %{_description}

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with check}
BuildRequires:  python2-pytest
BuildRequires:  python2-attrs
BuildRequires:  python2-pyasn1
BuildRequires:  python2-pyasn1-modules
BuildRequires:  pyOpenSSL
BuildRequires:  python2-idna
%endif
Requires:       python2-attrs
Requires:       python2-pyasn1
Requires:       python2-pyasn1-modules
Requires:       pyOpenSSL
Requires:       python2-idna

%description -n python2-%{modname} %{_description}

Python 2 version.

%if %{with python3}
%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with check}
BuildRequires:  python3-pytest
BuildRequires:  python3-attrs
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pyasn1-modules
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-idna
%endif
Requires:       python3-attrs
Requires:       python3-pyasn1
Requires:       python3-pyasn1-modules
Requires:       python3-pyOpenSSL
#Recommends:     python3-idna

%description -n python3-%{modname} %{_description}

Python 3 version.
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

#%if %{with check}
#%check
#PYTHONPATH=%{buildroot}%{python2_sitelib} py.test-%{python2_version} -v
#%if %{with python3}
#PYTHONPATH=%{buildroot}%{python3_sitelib} py.test-%{python3_version} -v
#%endif
#%endif

%files -n python2-%{modname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{srcname}-*.egg-info/
%{python2_sitelib}/%{srcname}/

%if %{with python3}
%files -n python3-%{modname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/
%endif

%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 16.0.0-6
- Rebuild for Python 3.6

* Mon Dec 19 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 16.0.0-5
- Modernize spec

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 16.0.0-4
- Enable tests

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 16.0.0-3
- Rebuild for Python 3.6
- Disable python3 tests for now

* Mon Oct 17 2016 Tom Prince <tom.prince@twistedmatrix.com> - 16.0.0-2
- Use python3 to test python3 package.
- Fix dependencies.

* Mon Oct 17 2016 Tom Prince <tom.prince@twistedmatrix.com> - 16.0.0-1
- Update source URL for pypi migration. (#1361604)
- Build new version

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 robyduck@fedoraproject.org - 14.0.0-1
- Build new version

* Sat Jul 12 2014 tom.prince@twistedmatrix.com - 1.0.0-2
- Add python-idna dependency.

* Sat Jul 12 2014 tom.prince@twistedmatrix.com - 1.0.0-1
- Initial package.
