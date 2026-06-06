cask "audx" do
  version "0.1.3"
  sha256 "009d2c87a9ddf9cbec8f34b9cc16a5d81706468faace7d9a1cd4678043c17480"

  url "https://github.com/kwong/audx/releases/download/v#{version}/audx-#{version}.dmg"
  name "audx"
  desc "Menu bar utility for switching audio input and output devices"
  homepage "https://github.com/kwong/audx"

  livecheck do
    url :url
    strategy :github_latest
  end

  app "audx.app"

  zap trash: [
    "~/Library/Application Support/audx",
    "~/Library/Caches/com.wkngw.audx",
    "~/Library/HTTPStorages/com.wkngw.audx",
    "~/Library/Preferences/com.wkngw.audx.plist",
    "~/Library/Saved Application State/com.wkngw.audx.savedState",
  ]
end
