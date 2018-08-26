%global srcname html5-parser
%global sum A fast, standards compliant, C based, HTML 5 parser for python

Name:           python-%{srcname}
Version:        0.4.4
Release:        4%{?dist}
Summary:        %{sum}

# html5-parser-0.4.4/gumbo/utf8.c is MIT
License:        ASL 2.0 and MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/h/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  python-devel 
BuildRequires:  libxml2-devel
BuildRequires:  pkgconfig
BuildRequires:  python-setuptools
# For tests
#BuildRequires:  python2-lxml >= 3.8.0
#BuildRequires:  gtest-devel
#BuildRequires:  python-chardet
#BuildRequires:  python-beautifulsoup4

%description
A fast, standards compliant, C based, HTML 5 parser for python

%package -n python2-%{srcname}
Summary:        %{sum}
Provides:      python2-%{srcname} = %{evrsion}

# This package bundles sigil-gumbo a fork of gumbo
# Base project: https://github.com/google/gumbo-parser
# Forked from above: https://github.com/Sigil-Ebook/sigil-gumbo
# It also patches that bundled copy with other changes.
# sigil-gumbo bundled here was added 20170601
Provides:      bundled(sigil-gumbo) = 0.9.3-20170601git0830e1145fe08
# sigil-gumbo forked off gumbo-parser at this commit in 20160216
Provides:      bundled(gumbo-parser) = 0.9.3-20160216git69b580ab4de04

%description -n python2-%{srcname}
A fast, standards compliant, C based, HTML 5 parser for python

%prep
export debug=True
%autosetup -n %{srcname}-%{version} -p1

# remove shebangs from library files
sed -i -e '/^#!\//, 1d' src/html5_parser/*.py

%build
%py2_build

%install
%py2_install

#%check
#%{__python2} setup.py test

%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitearch}/*


%changelog
* Wed Nov 08 2017 Kevin Fenzi <kevin@scrye.com> - 0.4.4-4
- Rebuild for upgrade path from f27

* Fri Oct 20 2017 Kevin Fenzi <kevin@scrye.com> - 0.4.4-3
- Adjust BuildRequires names for older releases

* Fri Oct 20 2017 Kevin Fenzi <kevin@scrye.com> - 0.4.4-2
- Clarify bundled copy of sigil-gumbo in spec comments.

* Sat Aug 12 2017 Kevin Fenzi <kevin@scrye.com> - 0.4.4-1
- Initial version for Fedora
