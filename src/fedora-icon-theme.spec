Summary: Fedora icon theme
Name: fedora-icon-theme
Version: 1.0.0
Release: 1%{?dist} 
BuildArch: noarch
License: GPL+
Group: User Interface/Desktops
# There is no official upstream yet
Source0: %{name}-%{version}.tar.bz2
URL: http://www.redhat.com
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

BuildRequires: perl(XML::Parser)
Requires: gnome-themes

Provides: system-icon-theme

%description
This package contains the Fedora icon theme.

%prep
%setup -q 

%build
%configure 
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# We provide the redhat files in pixmaps for backward compat,
# and so they're available for all themes. 
# If we didn't care about backward compat, then hicolor would
# be better than pixmaps
(cd $RPM_BUILD_DIR%{_datadir}/pixmaps;
   for icon in ../icons/Fedora/48x48/apps/{redhat-,temp-home}*.png; do
       ln -s $icon .
   done
)

# These are empty
rm -f ChangeLog NEWS README

# The upstream packages may gain po files at some point in the near future
%find_lang %{name} || touch %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/Fedora
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache -f --quiet %{_datadir}/icons/Fedora || :
fi

%postun
touch --no-create %{_datadir}/icons/Fedora
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache -f --quiet %{_datadir}/icons/Fedora || :
fi

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING
%{_datadir}/icons/Fedora
%{_datadir}/pixmaps/*.png

%changelog
* Tue Sep 25 2007 Ray Strode <rstrode@redhat.com> - 1.0.0-1
- Initial import, version 1.0.0
