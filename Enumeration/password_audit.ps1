param (
    [switch]$CheckUserPasswords,
    [switch]$AuditPasswordPolicy,
    [switch]$CheckServiceAccountPasswords
)

# Function to check password expiry for domain users
function Check-UserPasswordExpiry {
    Write-Host "Checking password expiry for domain users..."

    $passwordExpiryThreshold = (Get-Date).AddDays(7)  # Adjust as needed (7 days before expiration)

    # Get all domain users and their password last set date
    $users = Get-ADUser -Filter * -Properties PasswordLastSet, PasswordNeverExpires

    $expiredUsers = $users | Where-Object {
        $_.PasswordNeverExpires -eq $false -and ($_.PasswordLastSet -lt (Get-Date).AddDays(-90))  # 90 days since last password set
    }

    if ($expiredUsers) {
        Write-Host "The following users have passwords that have not been updated in the last 90 days:"
        $expiredUsers | Select-Object Name, PasswordLastSet | Format-Table -AutoSize
    } else {
        Write-Host "All users have updated their passwords within the last 90 days."
    }
}

# Function to audit password policy settings
function Audit-PasswordPolicy {
    Write-Host "Auditing domain password policy settings..."

    $passwordPolicy = Get-ADDefaultDomainPasswordPolicy

    Write-Host "Password Policy Settings:"
    Write-Host "-------------------------------------"
    Write-Host "Minimum Password Length: $($passwordPolicy.MinPasswordLength)"
    Write-Host "Maximum Password Age (days): $($passwordPolicy.MaxPasswordAge.Days)"
    Write-Host "Minimum Password Age (days): $($passwordPolicy.MinPasswordAge.Days)"
    Write-Host "Password History Count: $($passwordPolicy.PasswordHistoryCount)"
    Write-Host "Account Lockout Threshold: $($passwordPolicy.LockoutThreshold)"
    Write-Host "Lockout Duration (minutes): $($passwordPolicy.LockoutDuration.Minutes)"
    Write-Host "Lockout Observation Window (minutes): $($passwordPolicy.LockoutObservationWindow.Minutes)"
}

# Function to detect expired service account passwords
function Check-ServiceAccountPasswords {
    Write-Host "Checking expired service account passwords..."

    # Get all service accounts
    $serviceAccounts = Get-ADServiceAccount -Filter * -Properties PasswordLastSet, Enabled

    $expiredServiceAccounts = $serviceAccounts | Where-Object {
        $_.Enabled -eq $true -and ($_.PasswordLastSet -lt (Get-Date).AddDays(-30))  # 30 days without password change
    }

    if ($expiredServiceAccounts) {
        Write-Host "The following service accounts have expired passwords:"
        $expiredServiceAccounts | Select-Object Name, PasswordLastSet | Format-Table -AutoSize
    } else {
        Write-Host "No service accounts with expired passwords detected."
    }
}

#Handles which function to execute - based on provided parameter
if ($CheckUserPasswords) {
    Check-UserPasswordExpiry
}

if ($AuditPasswordPolicy) { 
    Audit-PasswordPolicy
}

if ($CheckServiceAccountPasswords) {
    Check-ServiceAccountPasswords
}
