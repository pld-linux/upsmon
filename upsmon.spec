Summary:	Allows to monitor UPS from Fideltronik
Summary(pl):	Zapewnia monitoring UPSów firmy Fideltronik
Name:		upsmon
Version:	2.0
Release:	2
Epoch:		1
License:	Free
Group:		Daemons
Source0:	http://www.fideltronik.com.pl/pl_products/upsmon/software/20_linux/%{name}20s.tar
Source1:	%{name}.init
URL:		http://www.fideltronik.com.pl/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ups

%description
Allows to monitor UPS from Fideltronik.

%description -l pl
Zapewnia monitoring i bezpieczne zamkniêcie systemu operacyjnego
komputera z do³±czonym zasilaczem UPS, oraz powiadamianie stacji
roboczych z zainstalowanym UPS Monitor Client.

%prep
%setup -q -c %{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/scripts,/etc/rc.d/init.d,/var/log}

install upsmonitor/*.sh $RPM_BUILD_ROOT%{_sysconfdir}/scripts/
install upsmonitor/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/
install upsmonitor/upsd $RPM_BUILD_ROOT%{_sbindir}/fidel-upsd
install upsmonitor/upsoff $RPM_BUILD_ROOT%{_sbindir}/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsd

touch $RPM_BUILD_ROOT/var/log/ups.log
ln -sf /var/log/ups.log $RPM_BUILD_ROOT%{_sysconfdir}/ups.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add upsd
if [ -f /var/lock/subsys/upsd ]; then
        /etc/rc.d/init.d/upsd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/upsd start\" to start upsd daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/upsd ]; then
                /etc/rc.d/init.d/upsd stop 1>&2
        fi
        /sbin/chkconfig --del upsd
fi

%files
%defattr(644,root,root,755)
%doc czytaj.to
%attr(750,root,root) %{_sbindir}/*
%attr(750,root,root) %dir %{_sysconfdir}
%attr(750,root,root) %dir %{_sysconfdir}/scripts
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/scripts/*.sh
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/*.conf
%attr(644,root,root) %{_sysconfdir}/ups.log
%attr(755,root,root) /etc/rc.d/init.d/upsd
%ghost %attr(644,root,root) /var/log/ups.log
