#!/usr/bin/env python3
"""
Admin Account Verification Script
Verify that the admin account has been created correctly
"""

import sqlite3
import hashlib

def verify_admin_account():
    """Verify admin account credentials"""
    db_path = 'regenerative_addresses.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get admin user from database
        cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
        admin_user = cursor.fetchone()
        
        if admin_user:
            print("✅ Admin account found in database:")
            print(f"   Username: {admin_user[1]}")
            print(f"   Email: {admin_user[3]}")
            print(f"   Created: {admin_user[4]}")
            
            # Verify password hash
            test_password = "Toreyisnotlettingyoubeanadmin"
            test_hash = hashlib.sha256(test_password.encode()).hexdigest()
            stored_hash = admin_user[2]
            
            if test_hash == stored_hash:
                print("✅ Password hash verification: PASSED")
                print("✅ Admin account is ready for use!")
            else:
                print("❌ Password hash verification: FAILED")
                print(f"   Expected: {test_hash}")
                print(f"   Stored: {stored_hash}")
        else:
            print("❌ Admin account not found in database")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Show database summary
    print("\n📊 Database Summary:")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM links')
        link_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM proxies')
        proxy_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM activity_log')
        activity_count = cursor.fetchone()[0]
        
        print(f"   Users: {user_count}")
        print(f"   Links: {link_count}")
        print(f"   Proxies: {proxy_count}")
        print(f"   Activity Logs: {activity_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"   Error getting summary: {e}")

if __name__ == "__main__":
    print("🔐 DemonVPN Admin Account Verification")
    print("=" * 50)
    verify_admin_account()
    print("=" * 50)
