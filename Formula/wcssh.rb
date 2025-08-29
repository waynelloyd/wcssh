class Wcssh < Formula
  desc "A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default."
  homepage "https://github.com/waynelloyd/homebrew-wcssh"
  url "https://github.com/waynelloyd/homebrew-wcssh/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "57ccb7e72bab287bb70fb7d02337fe9c939031e6d94a9ae4e325ee0ebeda2dd2" # The checksum of the new v1.0.0 tarball
  license "MIT"

  def install
    bin.install "wcssh.py" => "wcssh"
  end

  test do
    system "#{bin}/wcssh", "--version"
  end
end
