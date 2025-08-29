class Wcssh < Formula
  desc "A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default."
  homepage "https://github.com/waynelloyd/homebrew-wcssh"
  url "https://github.com/waynelloyd/homebrew-wcssh/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "83e15b8198d0f3e5ba4c1a99e1c17f258c5dfebdbf39341e058a9392addaaa8a" # Replace this with the output of: shasum -a 256 v0.1.0.tar.gz
  license "MIT"

  def install
    bin.install "wcssh.py" => "wcssh"
  end

  test do
    system "#{bin}/wcssh", "--version"
  end
end
