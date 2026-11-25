cask "dictiq" do
  version "0.1.0"
  sha256 "df8277c101ec1f80ca0d328f10d416f298bc2fe65510d0e1da77e25a6a33e61f"

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
