cask "sortbook" do
  version "1.0.8"
  sha256 "82e0d1a4b23e4d113b2946b22bc7c4af5590d6b6c4001ff217f32d67c5219f3b"

  url "https://sortbook.app/download/Sortbook_#{version}_aarch64.dmg"
  name "Sortbook"
  desc "Move the files in your folders into subfolders by type, month or year"
  homepage "https://sortbook.app/"

  livecheck do
    url "https://sortbook.app/download/"
    regex(/Sortbook[._-]v?(\d+(?:\.\d+)+)[._-]aarch64\.dmg/i)
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :monterey

  app "Sortbook.app"

  zap trash: [
    "~/Library/Application Support/com.hardboundstudio.sortbook",
    "~/Library/Caches/com.hardboundstudio.sortbook",
    "~/Library/Preferences/com.hardboundstudio.sortbook.plist",
    "~/Library/WebKit/com.hardboundstudio.sortbook",
  ]
end
