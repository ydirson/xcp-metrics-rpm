Name:           xcp-metrics
Version:        0.0.0
Release:        el7.yd0
Summary:        Rust-based plugins for xcp-rrdd

License:        AGPL-3.0-only
URL:            https://github.com/xcp-ng/xcp-metrics/

# source + third-party/
Source0:        xcp-metrics-0.0.0.tar.gz
Source1:        xcp-metrics-0.0.0-vendor.tar.gz
# config for third-party/ usage
Source2:        cargo-config.toml

BuildRequires:  rust >= 1.66
BuildRequires:  cargo
BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  protobuf-devel
BuildRequires:  systemd-devel

%global _description %{expand:
%{summary}.}

%description %{_description}

%prep
# unpack Source[01]
%setup -b1
# use cargo config
mkdir .cargo
ln -rs %{_sourcedir}/cargo-config.toml .cargo/config.toml

%build
cargo --offline build --release

%install
# FIXME does not like this does not come from "cargo package"?
#cargo --offline install
%{__install} -m755 -d %{buildroot}%{_sbindir} %{buildroot}/opt/xensource/libexec/xcp-rrdd-plugins/
%{__install} -m755 target/release/xcp-metrics-plugin-squeezed %{buildroot}/%{_sbindir}
ln -rs %{buildroot}/%{_sbindir}/xcp-metrics-plugin-squeezed %{buildroot}/opt/xensource/libexec/xcp-rrdd-plugins/rrdp-squeezed
%{__install} -m 755 -d %{buildroot}%{_unitdir}
%{__install} -m 644 plugins/xcp-metrics-plugin-squeezed/src/rrdp-squeezed.service %{buildroot}%{_unitdir}

%if %{with check}
%check
cargo --offline test
%endif

%files
%{_sbindir}/xcp-metrics-plugin-squeezed
/opt/xensource/libexec/xcp-rrdd-plugins/rrdp-squeezed
%{_unitdir}/rrdp-squeezed.service

%post
%systemd_post rrdp-squeezed.service

%changelog
* Wed Aug 23 2023 Yann Dirson <yann.dirson@vates.tech> - 0.0.0-el7.yd0
- Initial packaging for demo purposes
