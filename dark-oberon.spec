%define	name	dark-oberon
%define	version	1.0.2
%define	pre	RC2
%define	release	0.rc2.2
%define	Summary	Dark Oberon

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Group:		Games/Strategy
Source0:	%{name}-%{version}-%{pre}.tar.lzma
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
#Patch0:		dark-oberon-1.0.2-RC1-mdkconf.patch.bz2
Patch1:		dark-oberon-1.0.2-rc2-compile-fixes.patch	
Url:		http://dark-oberon.sourceforge.net/
Summary:	%{Summary}
License:	GPL
BuildRequires:	X11-devel glfw Mesa-common-devel lzma
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Dark Oberon is an open source real-time strategy game similar to Warcraft II
released under GPL. It has got awesome graphics - textures created from
shots of real models made out of plasticine!

%prep
%setup -q -n %{name}-%{version}-%{pre}
#%patch0 -p1 -b .mdkconf
%patch1 -p0  -b .fixes
find -name CVS|xargs rm -rf
cd src
sh create_makefile.sh

%build
%make DEFINES="-DDATA_DIR='\"%{_gamesdatadir}/%{name}/\"' -DUNIX=1 -DSOUND=0 -DDEBUG=0" CPPFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -m755 dark-oberon -D $RPM_BUILD_ROOT%{_gamesbindir}/%{name}
install -d $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
cp -r dat maps races schemes -d $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}

install -d $RPM_BUILD_ROOT%{_menudir}
cat <<EOF >$RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="%{_gamesbindir}/%{name}" \
		icon="%{name}.png" \
		needs="x11" \
		section="More Applications/Games/Strategy" \
		title="Dark Oberon" \
		longtitle="%{Summary}"
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README docs/*
%{_gamesbindir}/*
%{_gamesdatadir}/%{name}
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
