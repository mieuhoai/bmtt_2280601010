from flask import Flask, request, jsonify
from cipher.rsa import RSACipher


app = Flask(__name__)

#RSA

rsa_cipher = RSACipher()

@app.route("/api/rsa/generate_keys", methods=["POST"])
def generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route("/api/rsa/encrypt", methods=["POST"])
def rsa_encrypt():
    data = request.json
    message = data['message']
    key_type = data['key_type']
    private_key, public_key = rsa_cipher.get_keys()
    if key_type == "public":
        key = public_key
    elif key_type == "private":
        key = private_key
    else:
        return jsonify({'message': 'Invalid key type'})
    encrypted_message = rsa_cipher.encrypt(message, key_type)
    encrypted_hex = encrypted_message.hex()
    return jsonify({'encrypted_message': encrypted_message})


@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key_type = data['key_type']
    private_key, public_key = rsa_cipher.load_keys()
    if key_type == "public":
        key = public_key
    elif key_type == "private":
        key = private_key
    else:
        return jsonify({'message': 'Invalid key type'})
    cipher_text = bytes.fromhex(cipher_text)
    decrypted_message = rsa_cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_message})


@app.route("/api/rsa/sign", methods=["POST"])
def rsa_sign():
    data = request.json
    message = data['message']
    private_key, _ = rsa_cipher.load_keys()
    signature = rsa_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})
    
@app.route("/api/rsa/verify", methods=["POST"])
def rsa_verify():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    _, public_key = rsa_cipher.load_keys()
    signature = bytes.fromhex(signature)
    is_verified = rsa_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)