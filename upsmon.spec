Summary:	Allows to monitor UPS from Fideltronik
Summary(pl):	Zapewnia monitoring UPSów firmy Fideltronik
Name:		upsmon
Version:	2.2
Release:	0.2
Epoch:		1
License:	Free
Group:		Daemons
Source0:	http://www.fideltronik.com.pl/pl_products/upsmon/software/2x_linux/%{name}22s.tar
Source1:	%{name}.init
Source2:    http://www.fideltronik.com.pl/pl_products/upsmon/software/2x_linux/%{name}20c.tar
Source3:	%{name}-client.init
Patch0:		upsmon-acfail.patch
Patch1:		upsmon-conf.patch
Patch2:		upsmon-message.patch
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

Wa¿niejsze cechy:
	* monitoring sygna³ów "awarii zasilania" i "baterii roz³adowanych"
	* bezpieczne zamkniêcie systemu operacyjnego
	* uruchamianie skryptów przy ka¿dej zmianie stanu zasilacza UPS
	* wy³±czenie zasilacza UPS po zamkniêciu systemu
	* zapis historii stanu zasilania "LOG"
	* informowanie stacji roboczych/serwerów w sieci LAN (TCP/IP)
	* prosta instalacja 

%package server
Summary:    UPS Monitor 2.2 Server
Group:	Daemons

%description server
Allows to monitor UPS from Fideltronik.

%description server -l pl
Zapewnia monitoring i bezpieczne zamkniêcie systemu operacyjnego
komputera z do³±czonym zasilaczem UPS, oraz powiadamianie stacji

%package client
Summary:	UPS Monitor 2.0 Client
Group:		Daemons
Version:	2.0

%description client
Allows to monitor UPS from Fideltronik.

%description client -l pl
UPS Monitor Client 2.0 jest programem odbieraj±cym komunikaty z modu³u
UPS Monitor Server 2.x poprzez TCP/IP i wykonuj±cym odpowiednie skrypty,
w których mo¿na zamie¶ciæ polecenie zamkniêcia lokalnego systemu.

Wa¿niejsze cechy:
	* obs³uga komunikatów TCP/IP z maksymalnie 5-ciu serwerów (UPS Monitor Server)
	* wykonywanie wybranego skryptu przy kazdej zmianie stanu zdalnego UPS-a
	* dedykowane skrypty dla ka¿dego zdalnego UPS-a
	* ³atwa konfiguracja w pliku tekstowym
	* prosta instalacja 

%prep
%setup -q -c %{name}-%{version} -a2
%patch0
%patch1
%patch2

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/sbin,%{_sysconfdir}/scripts,/etc/rc.d/init.d,/var/log}

install server/scripts/* $RPM_BUILD_ROOT%{_sysconfdir}/scripts/
install server/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/
install server/upsd $RPM_BUILD_ROOT%{_sbindir}/fidel-upsd
install server/upsoff $RPM_BUILD_ROOT/sbin/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsd
install server/upsd.log $RPM_BUILD_ROOT/var/log/upsd.log

ln -sf /var/log/upsd.log $RPM_BUILD_ROOT%{_sysconfdir}/upsd.log 

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/server{1,2,3,4,5},/etc/rc.d/init.d}
install client/server1/*.sh $RPM_BUILD_ROOT%{_sysconfdir}/server1/
for i in 2 3 4 5; do
	cp $RPM_BUILD_ROOT%{_sysconfdir}/server1/* $RPM_BUILD_ROOT%{_sysconfdir}/server${i}/
done
install client/upsc.conf $RPM_BUILD_ROOT%{_sysconfdir}/
install client/upsc $RPM_BUILD_ROOT%{_sbindir}/fidel-upsc
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsc

%clean
rm -rf $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add upsd
if [ -f /var/lock/subsys/upsd ]; then
        /etc/rc.d/init.d/upsd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/upsd start\" to start upsd daemon."
fi

%preun server
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/upsd ]; then
                /etc/rc.d/init.d/upsd stop 1>&2
        fi
        /sbin/chkconfig --del upsd
fi

%post client
/sbin/chkconfig --add upsc
if [ -f /var/lock/subsys/upsc ]; then
        /etc/rc.d/init.d/upsc restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/upsc start\" to start upsc daemon."
fi

%preun client
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/upsc ]; then
                /etc/rc.d/init.d/upsc stop 1>&2
        fi
        /sbin/chkconfig --del upsc
fi

%files server
%defattr(644,root,root,755)
%doc czytaj.to
%attr(750,root,root) %{_sbindir}/fidel-upsd
%attr(750,root,root) /sbin/upsoff
%attr(750,root,root) %dir %{_sysconfdir}
%attr(750,root,root) %dir %{_sysconfdir}/scripts
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/scripts/*.sh
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsd.conf
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsoff.conf
%ghost %attr(644,root,root) %{_sysconfdir}/upsd.log
%attr(755,root,root) /etc/rc.d/init.d/upsd
%attr(644,root,root) /var/log/upsd.log

%files client
%defattr(644,root,root,755)
%doc czytaj.to
%attr(750,root,root) %{_sbindir}/fidel-upsc
%attr(750,root,root) %dir %{_sysconfdir}
%attr(750,root,root) %dir %{_sysconfdir}/server1
%attr(750,root,root) %dir %{_sysconfdir}/server2
%attr(750,root,root) %dir %{_sysconfdir}/server3
%attr(750,root,root) %dir %{_sysconfdir}/server4
%attr(750,root,root) %dir %{_sysconfdir}/server5
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/server1/*.sh
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/server2/*.sh
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/server3/*.sh
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/server4/*.sh
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/server5/*.sh
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsc.conf
%attr(755,root,root) /etc/rc.d/init.d/upsc
