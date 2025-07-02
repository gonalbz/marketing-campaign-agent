while read -r line; do
  # Ignora comentarios y líneas vacías
  [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
  echo "→ Agregando $line al uv.toml"
  uv add "$line"
done < requirements.txt
