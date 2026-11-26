cask "dictiq" do
  version "0.5.0"
  sha256 "59b3db3934e2050ef24fd9ee68ce7c3139c6575c91572b7be7468ea1f0de1761"

  url "https://hardboundstudio.com/downloads/dictiq/Dictiq-#{version}-macOS.zip"
  name "Dictiq"
  desc "On-device dictation"
  homepage "https://dictiq.app/"

  livecheck do
    url "https://dictiq.app/"
    regex(/Dictiq[._-]v?(\d+(?:\.\d+)+)[._-]macOS\.zip/i)
  end

  depends_on arch: :arm64
  depends_on macos: :ventura

  app "Dictiq.app"

  zap trash: [
    "~/Library/Application Support/app.dictiq.desktop",
    "~/Library/Caches/app.dictiq.desktop",
    "~/Library/Preferences/app.dictiq.desktop.plist",
  ]
end
