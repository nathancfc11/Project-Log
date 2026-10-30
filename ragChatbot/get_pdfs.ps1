# get_pdfs.ps1 - downloads the starter corpus into data\pdfs
$ua = "Mozilla/5.0"
$pdfs = [ordered]@{
    "nist-sp800-63b-4-passwords-authentication.pdf" = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63B-4.pdf"
    "nist-sp800-61r3-incident-response.pdf"         = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf"
    "nist-sp800-83r1-malware.pdf"                   = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-83r1.pdf"
    "nist-sp800-40r4-patching.pdf"                  = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-40r4.pdf"
    "nist-sp800-124r2-mobile-devices.pdf"           = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-124r2.pdf"
    "nist-sp800-46r2-remote-access.pdf"             = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-46r2.pdf"
    "nist-sp800-114r1-home-devices.pdf"             = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-114r1.pdf"
    "nist-sp800-50r1-security-awareness.pdf"        = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-50r1.pdf"
    "nist-csf-2.0.pdf"                              = "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf"
    "cisa-phishing-guidance.pdf"                    = "https://www.cisa.gov/sites/default/files/2023-10/Phishing%20Guidance%20-%20Stopping%20the%20Attack%20Cycle%20at%20Phase%20One_508c.pdf"
    "cisa-phishing-postcard.pdf"                    = "https://www.cisa.gov/sites/default/files/2024-02/Update%20to%20Phishing%20General%20Security%20Postcard_01.01.2024.pdf"
    "ncsc-top-tips-for-staff.pdf"                   = "https://www.ncsc.gov.uk/sites/default/files/2026-08/Top-Tips-for-Staff-help-your-staff-keep-your-organisation-safe-online.pdf"
    "ncsc-small-charity-guide.pdf"                  = "https://www.ncsc.gov.uk/files/Charity-Guide-v3.pdf"
}

foreach ($name in $pdfs.Keys) {
    $out = "data\pdfs\$name"
    if (Test-Path $out) { Write-Output "skip $name (already have it)"; continue }
    try {
        Invoke-WebRequest -Uri $pdfs[$name] -OutFile $out -UserAgent $ua
        $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $out))
        if ([System.Text.Encoding]::ASCII.GetString($bytes[0..3]) -ne "%PDF") {
            Remove-Item $out
            Write-Output "FAIL $name (got a web page, not a PDF)"
        } else {
            Write-Output "ok   $name"
        }
    } catch {
        Write-Output "FAIL $name ($($_.Exception.Message))"
    }
}