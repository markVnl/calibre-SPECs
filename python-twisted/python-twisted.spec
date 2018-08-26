%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-twisted
Version:        16.4.1
Release:        5%{?dist}
Summary:        Twisted is a networking engine written in Python
License:        MIT
URL:            http://twistedmatrix.com/
Source0:        https://files.pythonhosted.org/packages/source/T/Twisted/Twisted-%{version}.tar.bz2


%description
Twisted is a networking engine written in Python, supporting numerous protocols.
It contains a web server, numerous chat clients, chat servers, mail servers
and more.


%package -n python2-twisted
Summary:        %{summary}
%{?python_provide:%python_provide python2-twisted}

BuildRequires:  python2-devel >= 2.6
BuildRequires:  python-zope-interface >= 3.6.0
BuildRequires:  python-crypto >= 2.6.1
BuildRequires:  pyOpenSSL >= 0.10
BuildRequires:  python-service-identity
BuildRequires:  python-setuptools

Requires:       python-zope-interface >= 3.6.0
Requires:       pyOpenSSL >= 0.10
Requires:       python-service-identity

# Bring all provided resources back into the main package namespace.
Obsoletes:      python-twisted-conch < 14
Provides:       python-twisted-conch = %{version}-%{release}
Obsoletes:      python-twisted-core < 14
Provides:       python-twisted-core = %{version}-%{release}
Obsoletes:      python-twisted-core-doc < 14
Provides:       python-twisted-core-doc = %{version}-%{release}
Obsoletes:      python-twisted-lore < 14
# obsolete-not-provided: Lore has been removed completely upstream
Obsoletes:      python-twisted-mail < 14
Provides:       python-twisted-mail = %{version}-%{release}
Obsoletes:      python-twisted-names < 14
Provides:       python-twisted-names = %{version}-%{release}
Obsoletes:      python-twisted-news < 14
Provides:       python-twisted-news = %{version}-%{release}
Obsoletes:      python-twisted-runner < 14
Provides:       python-twisted-runner = %{version}-%{release}
Obsoletes:      python-twisted-web < 14
Provides:       python-twisted-web = %{version}-%{release}
Obsoletes:      python-twisted-web2 < 14
Provides:       python-twisted-web2 = %{version}-%{release}
Obsoletes:      python-twisted-words < 14
Provides:       python-twisted-words = %{version}-%{release}

# Capture previous namespace.
Obsoletes:      Twisted < 2.4.0-1
Provides:       Twisted = %{version}-%{release}
Obsoletes:      twisted < 2.4.0-1
Provides:       twisted = %{version}-%{release}

# python-twisted-conch
Requires:       python-crypto
Requires:       python-pyasn1

# python-twisted-core
Requires:       pyserial


%description -n python2-twisted
Twisted is a networking engine written in Python, supporting numerous protocols.
It contains a web server, numerous chat clients, chat servers, mail servers
and more.


%if 0%{?with_python3}
%package -n python3-twisted
Summary:        %{summary}
Requires:       python3-zope-interface
%{?python_provide:%python_provide python3-twisted}

BuildRequires:  python3-devel >= 3.3
BuildRequires:  python3-zope-interface >= 4.0.2
BuildRequires:  python3-crypto >= 2.6.1
BuildRequires:  python3-pyOpenSSL >= 0.10
BuildRequires:  python3-service-identity
BuildRequires:  python3-setuptools

Requires:       python3-zope-interface >= 3.6.0
Requires:       python3-pyOpenSSL >= 0.10
Requires:       python3-service-identity

# python-twisted-conch
Requires:       python3-crypto
Requires:       python3-pyasn1

# python-twisted-core
Requires:       python3-pyserial


%description -n python3-twisted
Twisted is a networking engine written in Python, supporting numerous protocols.
It contains a web server, numerous chat clients, chat servers, mail servers
and more.
%endif


%prep
%setup -q -n Twisted-%{version}


%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build


%install
%if 0%{?with_python3}
%py3_install

# Move and symlink python3 scripts
# no-manual-page-for-binary: man page is trial and twistd
mv %{buildroot}%{_bindir}/trial %{buildroot}%{_bindir}/trial-%{python3_version}
ln -s ./trial-%{python3_version} %{buildroot}%{_bindir}/trial-3

mv %{buildroot}%{_bindir}/twistd %{buildroot}%{_bindir}/twistd-%{python3_version}
ln -s ./twistd-%{python3_version} %{buildroot}%{_bindir}/twistd-3
%endif

%py2_install

# Packages that install arch-independent twisted plugins install here.
# https://bugzilla.redhat.com/show_bug.cgi?id=1252140
%{__mkdir_p} %{buildroot}%{python2_sitelib}/twisted/plugins
%if 0%{?with_python3}
%{__mkdir_p} %{buildroot}%{python3_sitelib}/twisted/plugins
%endif

# no-manual-page-for-binary
%{__mkdir_p} %{buildroot}%{_mandir}/man1/
for s in conch core mail; do
%{__cp} -a docs/$s/man/*.1 %{buildroot}%{_mandir}/man1/
done

# devel-file-in-non-devel-package
%{__rm} -v %{buildroot}%{python2_sitearch}/twisted/test/raiser.c
%{__rm} -v %{buildroot}%{python2_sitearch}/twisted/internet/iocpreactor/iocpsupport/winsock_pointers.c
%{__rm} -v %{buildroot}%{python2_sitearch}/twisted/internet/iocpreactor/iocpsupport/winsock_pointers.h
%{__rm} -v %{buildroot}%{python2_sitearch}/twisted/internet/iocpreactor/iocpsupport/iocpsupport.c
%{__rm} -v %{buildroot}%{python2_sitearch}/twisted/python/_sendmsg.c
%{__rm} -v %{buildroot}%{python2_sitearch}/twisted/runner/portmap.c

%if 0%{?with_python3}
%{__rm} -v %{buildroot}%{python3_sitearch}/twisted/test/raiser.c
%{__rm} -v %{buildroot}%{python3_sitearch}/twisted/internet/iocpreactor/iocpsupport/winsock_pointers.c
%{__rm} -v %{buildroot}%{python3_sitearch}/twisted/internet/iocpreactor/iocpsupport/winsock_pointers.h
%{__rm} -v %{buildroot}%{python3_sitearch}/twisted/internet/iocpreactor/iocpsupport/iocpsupport.c
%{__rm} -v %{buildroot}%{python3_sitearch}/twisted/python/_sendmsg.c
%{__rm} -v %{buildroot}%{python3_sitearch}/twisted/runner/portmap.c
%endif

# pem-certificate
# Needed for self-tests.

# wrong-script-interpreter
# pop3testserver.py: applies to py2.4 and that is the current default
# scripttest.py: is noop

# non-executable-script
%{__chmod} +x %{buildroot}%{python2_sitearch}/twisted/mail/test/pop3testserver.py
%{__chmod} +x %{buildroot}%{python2_sitearch}/twisted/trial/test/scripttest.py

# non-standard-executable-perm
%{__chmod} 755 %{buildroot}%{python2_sitearch}/twisted/python/_sendmsg.so
%{__chmod} 755 %{buildroot}%{python2_sitearch}/twisted/runner/portmap.so
%{__chmod} 755 %{buildroot}%{python2_sitearch}/twisted/test/raiser.so

# Move and symlink python2 scripts
# no-manual-page-for-binary: man page is trial and twistd
mv %{buildroot}%{_bindir}/trial %{buildroot}%{_bindir}/trial-%{python2_version}
ln -s ./trial-%{python2_version} %{buildroot}%{_bindir}/trial-2
ln -s ./trial-%{python2_version} %{buildroot}%{_bindir}/trial

mv %{buildroot}%{_bindir}/twistd %{buildroot}%{_bindir}/twistd-%{python2_version}
ln -s ./twistd-%{python2_version} %{buildroot}%{_bindir}/twistd-2
ln -s ./twistd-%{python2_version} %{buildroot}%{_bindir}/twistd


%check
# bin/trial twisted
# can't get this to work within the buildroot yet due to multicast
# https://twistedmatrix.com/trac/ticket/7494


%files -n python2-twisted
%doc CONTRIBUTING NEWS README.rst
%license LICENSE
%{_bindir}/cftp
%{_bindir}/ckeygen
%{_bindir}/conch
%{_bindir}/mailmail
%{_bindir}/pyhtmlizer
%{_bindir}/tkconch
%{_bindir}/trial
%{_bindir}/twist
%{_bindir}/twistd
%{_bindir}/trial-2*
%{_bindir}/twistd-2*
%{_mandir}/man1/cftp.1*
%{_mandir}/man1/ckeygen.1*
%{_mandir}/man1/conch.1*
%{_mandir}/man1/mailmail.1*
%{_mandir}/man1/pyhtmlizer.1*
%{_mandir}/man1/tkconch.1*
%{_mandir}/man1/trial.1*
%{_mandir}/man1/twistd.1*
%{python2_sitearch}/*
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-twisted
%doc CONTRIBUTING NEWS README.rst
%license LICENSE
%{_bindir}/trial-3*
%{_bindir}/twistd-3*
%{python3_sitearch}/*
%{python3_sitelib}/*
%endif


%changelog
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 16.4.1-2
- rebuilt

* Wed Oct 26 2016 Jonathan Steffan <jsteffan@fedoraproject.org> - 16.4.1-1
- Update to 16.4.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 16.3.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 8 2016 Jonathan Steffan <jsteffan@fedoraproject.org> - 16.3.0-1
- Update to 16.3.0
- mahole, tap2deb, tap2rpm are removed upstream

* Sun Jun 26 2016 Jonathan Steffan <jsteffan@fedoraproject.org> - 16.2.0-2
- Add rpmlint notes
- Fix unneeded py3 conditional for py2 script chmod

* Sun Jun 26 2016 Jonathan Steffan <jsteffan@fedoraproject.org> - 16.2.0-1
- Update to 16.2.0
- Update upstream source location

* Thu Jun  2 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 16.1.1-3
- Drop tkinter dependency (only required for tkconch)
- Use python3 conditionals
- Move BR under the proper subpackage

* Tue May 10 2016 Petr Viktorin <pviktori@redhat.com> - 16.1.1-2
- Update to better conform to Python packaging guidelines

* Thu May 05 2016 Julien Enselme <jujens@jujens.eu> - 16.1.1-1
- Update to 16.1.1 (#1287381)

* Thu Mar 10 2016 Julien Enselme <jujens@jujens.eu> - 15.5.0-2
- Add python3 support

* Thu Mar 10 2016 Julien Enselme <jujens@jujens.eu> - 15.5.0-1
- Update to 15.5.0 (#1287381)
- Use new python macros
- Remove deprecated %%clean section

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Tom Prince <tom.prince@twistedmatrix.com> - 15.4.0-2
- Add arch-independent plugin directory to package. (RHBZ#1252140)

* Thu Oct 29 2015 Tom Prince <tom.prince@twistedmatrix.com> - 15.4.0-1
- Update to 15.4.0
- Include test certificates.

* Mon Jul 20 2015 Jonathan Steffan <jsteffan@fedoraproject.org> - 15.2.1-1
- Update to 15.2.1

* Sat May 09 2015 Jonathan Steffan <jsteffan@fedoraproject.org> - 15.1.0-1
- Update to 15.1.0 (RHBZ#1187921,RHBZ#1192707)
- Require python-service-identity (RHBZ#1119067)
- Obsolete python-twisted-core-doc (RHBZ#1187025)

* Sat Nov 22 2014 Jonathan Steffan <jsteffan@fedoraproject.org> - 14.0.2-1
- Update to 14.0.2 (RHBZ#1143002)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Jonathan Steffan <jsteffan@fedoraproject.org> - 14.0.0-1
- Update to 14.0.0
- Ship Twisted as a fully featured package without subpackages on the advice
  of upstream and to mirror what pypi provides
- Explictly build for python2 with new macros

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 03 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.2.0-1
- Updated to 12.2.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.1.0-1
- Updated to 12.1.0

* Sun Feb 12 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.0.0-1
- Updated to 12.0.0

* Sat Jan 07 2012 Julian Sikorski <belegdol@fedoraproject.org> - 11.1.0-2
- Rebuilt for gcc-4.7

* Fri Nov 18 2011 Julian Sikorski <belegdol@fedoraproject.org> - 11.1.0-1
- Updated to 11.1.0
- Dropped obsolete Group, Buildroot, %%clean and %%defattr

* Sat Apr 30 2011 Julian Sikorski <belegdol@fedoraproject.org> - 11.0.0-1
- Updated to 11.0.0
- Added comment on how to obtain the PKG-INFO file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 10.2.0-1
- Updated to 10.2.0

* Mon Nov 08 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-3
- Use python_sitelib instead of python-sitearch
- The aforementioned macros are defined in Fedora 13 and above

* Sun Nov 07 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-2
- Added egg-info file

* Tue Sep 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-1
- Updated to 10.1.0
- Switched to macros for versioned dependencies

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matthias Saou <http://freshrpms.net/> 8.2.0-1
- Update to 8.2.0.
- Change back spec cosmetic details from Paul's to Thomas' preference.

* Wed Jul 16 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-2
- Update to 8.1.0.
- Minor spec file cleanups.
- Merge back changes from Paul Howarth.

* Wed May 21 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.5.0-1
- update to 2.5.0 release (only the umbrella package was missing)

* Tue Jan 16 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.4.0-3
- list packages in README.fedora

* Wed Jan 03 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.4.0-2
- add a README.fedora
- made noarch, since it doesn't actually install any python twisted/ module
  code
- fixed provides/obsoletes

* Wed Jun 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.4.0-1
- this is now a pure umbrella package

* Mon Oct 10 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.1.0-1
- upstream release

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.1-1
- upstream release

* Mon Apr 04 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-2
- add zsh support

* Fri Mar 25 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-1
- final release

* Thu Mar 17 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-0.2.a3
- dropped web2

* Wed Mar 16 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-0.1.a3
- upstream release

* Sat Mar 12 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-0.1.a2
- new prerelease; FE versioning

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0a1-1
- prep for split

* Fri Aug 20 2004 Jeff Pitman <symbiont+pyvault@berlios.de> 1.3.0-1
- new version

* Mon Apr 19 2004 Jeff Pitman <symbiont+pyvault@berlios.de> 1.2.0-3
- vaultize

* Mon Apr 12 2004 Jeff Pitman <symbiont+pyvault@berlios.de> 1.2.0-2
- require pyOpenSSL, SOAPpy, openssh-clients, crypto, dia so trial can run

