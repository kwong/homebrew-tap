cask "audx" do
  version "0.2.0"
  sha256 "1e2761657bfb5421a75c6286e638b1a588de40959f55175627a0a739398e4ef4"

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
