%global srcname cssutils

# Some tests are requiring internet access, disable everything for now
%bcond_with tests

Name:           python-%{srcname}
Summary:        CSS Cascading Style Sheets library for Python
Version:        1.0.1
Release:        8%{?dist}

License:        LGPLv3+
URL:            http://cthedot.de/cssutils/
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz

%if %{with tests}
# We don't really need pbr for testing
Patch0:         %{srcname}-remove-pbr.patch
# We always want use setuptools's use2to3 option
Patch1:         %{srcname}-use2to3.patch
%endif

BuildArch:      noarch

BuildRequires:  dos2unix

%global _description \
A Python package to parse and build CSS Cascading Style Sheets. DOM only, not\
any rendering facilities.

%description %{_description}

%package doc
Summary:        Documentation for %{name}

%description doc
%{summary}.

%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with tests}
BuildRequires:  python2-mock
%endif

%description -n python2-%{srcname} %{_description}

Python 2 version.

%prep
%setup -c
pushd %{srcname}-%{version}
%autopatch -p1
cp -a {README.txt,COPYING,examples/} ..
rm -rf src/%{srcname}.egg-info
popd
# Convert all CRLF files, keeping original timestamps
find -type f -exec dos2unix -k {} ';'
# Shebang is useless, there are two groups of files:
# 1. Scripts which are installed as entry_points
# 2. Normal files
# None of those require shebang
find -type f -name '*.py' -exec sed -i -e '1{\@^#!/usr/bin/env python@d}' {} ';'
mv %{srcname}-%{version} python2
cp -a python2 python3

%build
pushd python2
  %py2_build
popd


%install
pushd python2
  %py2_install
popd
rm -vrf %{buildroot}%{python2_sitelib}/%{srcname}/tests/

%if %{with tests}
%check
pushd python2
  %{__python2} setup.py test -v
popd
%endif

%files -n python2-%{srcname}
%license COPYING
%doc README.txt
%{python2_sitelib}/%{srcname}-*.egg-info/
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/encutils/
%{_bindir}/csscapture
%{_bindir}/csscombine
%{_bindir}/cssparse

%files doc
%doc examples/

%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-6
- Rebuild for Python 3.6

* Sat Aug 27 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.1-5
- Fixes in packaging
- Run test suite
- Don't distribute test suite
- Cleanups

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Mar 06 2016 Kevin Fenzi <kevin@scrye.com> - 1.0.1-3
- Create python2 and python3 subpackages. Fixes bug #1310629

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 26 2015 Kevin Fenzi <kevin@scrye.com> - 1.0.1-1
- Update to 1.0.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 04 2012 Kevin Fenzi <kevin@scrye.com> - 0.9.9-1
- Update to 0.9.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Kevin Fenzi <kevin@tummy.com> - 0.9.7-1
- Update to final 0.9.7

* Sun Sep 12 2010 Kevin Fenzi <kevin@tummy.com> - 0.9.7-0.0.b3
- Update to 0.9.7 beta 3

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Feb 25 2010 Matthias Saou <http://freshrpms.net/> 0.9.6-1
- Update to 0.9.6.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.5.1-4
- Rebuild for Python 2.6

* Fri Oct 10 2008 Matthias Saou <http://freshrpms.net/> 0.9.5.1-3
- Add missing python-setuptools BR, split off doc sub-package (mschwendt).

* Thu Oct  9 2008 Matthias Saou <http://freshrpms.net/> 0.9.5.1-2
- Update license, group, add python-setuptools requirement (mschwendt).

* Tue Aug 19 2008 Matthias Saou <http://freshrpms.net/> 0.9.5.1-1
- Update to 0.9.5.1.

* Fri Aug  8 2008 Matthias Saou <http://freshrpms.net/> 0.9.5-1
- Update to 0.9.5 final.

* Tue Jul 15 2008 Matthias Saou <http://freshrpms.net/> 0.9.5b2-0.2.rc2
- Convert CRLF end of lines.
- Patch out #!/... magic from python files meant to be included and not run.

* Tue Jul 15 2008 Matthias Saou <http://freshrpms.net/> 0.9.5b2-0.1.rc2
- Initial RPM release.

