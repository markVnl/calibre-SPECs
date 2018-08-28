Name:           odfpy
Version:        1.3.4
Release:        3%{?dist}
Summary:        Python library for manipulating OpenDocument files

License:        GPLv2+
URL:            https://github.com/eea/odfpy
Source0:        https://github.com/eea/%{name}/archive/release-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Odfpy aims to be a complete API for OpenDocument in Python. Unlike
other more convenient APIs, this one is essentially an abstraction
layer just above the XML format. The main focus has been to prevent
the programmer from creating invalid documents. It has checks that
raise an exception if the programmer adds an invalid element, adds an
attribute unknown to the grammar, forgets to add a required attribute
or adds text to an element that doesn't allow it.

These checks and the API itself were generated from the RelaxNG
schema, and then hand-edited. Therefore the API is complete and can
handle all ODF constructions, but could be improved in its
understanding of data types.

%package -n python2-%{name}
Summary:        %{summary}

BuildRequires:  python-devel
BuildRequires:  python-setuptools

Provides:       odfpy = %{version}-%{release}
Obsoletes:      odfpy < %{version}-%{release}
Provides:       python2-%{name} = %{version}-%{release}

%description -n python2-%{name}
Odfpy aims to be a complete API for OpenDocument in Python. Unlike
other more convenient APIs, this one is essentially an abstraction
layer just above the XML format. The main focus has been to prevent
the programmer from creating invalid documents. It has checks that
raise an exception if the programmer adds an invalid element, adds an
attribute unknown to the grammar, forgets to add a required attribute
or adds text to an element that doesn't allow it.
 
These checks and the API itself were generated from the RelaxNG
schema, and then hand-edited. Therefore the API is complete and can
handle all ODF constructions, but could be improved in its
understanding of data types.

This package provides Python 2 build of %{name}.

%package doc
Summary:        %{summary}

%description doc
Odfpy aims to be a complete API for OpenDocument in Python. Unlike
other more convenient APIs, this one is essentially an abstraction
layer just above the XML format. The main focus has been to prevent
the programmer from creating invalid documents. It has checks that
raise an exception if the programmer adds an invalid element, adds an
attribute unknown to the grammar, forgets to add a required attribute
or adds text to an element that doesn't allow it.

These checks and the API itself were generated from the RelaxNG
schema, and then hand-edited. Therefore the API is complete and can
handle all ODF constructions, but could be improved in its
understanding of data types.

This package provides documentation of %{name}.

%prep
%autosetup -n %{name}-release-%{version}
# Change shebang in all relevant files
find -type f -exec sed -i '1s=^#!/usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +

%build
%py2_build

%install
%py2_install
rm %{buildroot}%{_bindir}/*

#%check
#make --directory tests

%files -n python2-%{name}
%license GPL-LICENSE-2.txt APACHE-LICENSE-2.0.txt
%{_mandir}/man1/*
%{python2_sitelib}/*egg-info
%{python2_sitelib}/odf

%files doc
%license GPL-LICENSE-2.txt APACHE-LICENSE-2.0.txt
%doc doc examples contrib

%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 13 2017 Charalampos Stratakis <cstratak@redhat.com> 1.3.4-2
- Add proper provides and obsoletes for a clean upgrade path after
renaming the python2 subpackage

* Fri Mar 3 2017 Iryna Shcherbina <ishcherb@redhat.com> 1.3.4-1
- Update to 1.3.4, run tests

* Fri Mar 3 2017 Jan Beran <jberan@redhat.com> 1.3.3-1
- New version including Python 3 subpackage

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Kevin Fenzi <kevin@scrye.com> 0.9.6-1
- Update to 0.9.6 Fixes calibre bug #989538

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.2-7
- Fix FTBFS

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 30 2010 Ian Weller <iweller@redhat.com> - 0.9.2-2
- Fixed previous changelog entry

* Fri Jul 30 2010 Ian Weller <iweller@redhat.com> - 0.9.2-1
- Update to 0.9.2

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Ian Weller <ianweller@gmail.com> - 0.9-1
- Update upstream

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8-2
- Rebuild for Python 2.6

* Fri Aug 22 2008 Ian Weller <ianweller@gmail.com> 0.8-1
- Update upstream

* Tue Jul 15 2008 Ian Weller <ianweller@gmail.com> 0.7-2
- Change macros
- Remove license file

* Sun Jul 13 2008 Ian Weller <ianweller@gmail.com> 0.7-1
- Add COPYING file
- Use setuptools instead
- sed out shebangs from module files
- Other minor fixes

* Sun Jul 13 2008 Paul W. Frields <stickster@gmail.com> - 0.7-0.1
- Initial RPM package
