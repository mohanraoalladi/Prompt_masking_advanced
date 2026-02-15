"""Color mapping for different PII entity types"""

ENTITY_COLORS = {
    "PERSON": "#FF6B6B",  # Red
    "EMAIL_ADDRESS": "#4ECDC4",  # Teal
    "PHONE_NUMBER": "#45B7D1",  # Blue
    "LOCATION": "#FFA07A",  # Light Salmon
    "CLIENT_ID": "#98D8C8",  # Mint Green
    "ACCOUNT_REFERENCE": "#F7DC6F",  # Yellow
    "IP_ADDRESS": "#BB8FCE",  # Purple
    "ORGANIZATION": "#F8B88B",  # Peach
    "CREDIT_CARD": "#85C1E2",  # Light Blue
    "URL": "#82E0AA",  # Light Green
}

def get_entity_color(entity_type: str) -> str:
    """Get color for entity type"""
    return ENTITY_COLORS.get(entity_type, "#D3D3D3")

def colorize_masked_text(text: str, mapping: dict) -> str:
    """
    Build colored HTML with proper text display
    
    Args:
        text: Text with placeholders
        mapping: Dictionary mapping placeholders to original values
    
    Returns:
        HTML string with colored and visible placeholders
    """
    result = text
    
    # Sort by length (longer first) to avoid replacing partial matches
    sorted_items = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)
    
    for placeholder, original_value in sorted_items:
        # Extract entity type
        entity_type = placeholder.strip("<>").rsplit("_", 1)[0]
        color = get_entity_color(entity_type)
        
        # Create HTML with visible placeholder text
        escaped_value = original_value.replace('"', '&quot;').replace("'", "&#39;")
        # Escape placeholder for HTML so angle brackets are visible
        escaped_placeholder = placeholder.replace('<', '&lt;').replace('>', '&gt;')
        # Use background color with visible text and border
        html_span = (
            f'<span style="'
            f'background-color: {color}; '
            f'color: white; '
            f'padding: 3px 6px; '
            f'border-radius: 3px; '
            f'font-weight: 700; '
            f'font-size: 12px; '
            f'cursor: help; '
            f'border: 1px solid rgba(0,0,0,0.2); '
            f'white-space: nowrap;'
            f'" title="{escaped_value}">●{escaped_placeholder}</span>'
        )
        
        result = result.replace(placeholder, html_span)
    
    # Wrap in pre-formatted text to preserve line breaks and spacing
    result = result.replace('\n', '<br/>')
    return f'<div style="line-height: 1.8; word-wrap: break-word; font-family: Arial, sans-serif;">{result}</div>'

def get_color_legend() -> str:
    """Generate HTML color legend"""
    legend_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 15px 0;">'
    
    for entity_type, color in ENTITY_COLORS.items():
        legend_html += f'''<div style="display: flex; align-items: center; gap: 8px; padding: 8px; background: #f9f9f9; border-radius: 4px; border: 1px solid #e0e0e0;">
            <span style="display: inline-block; width: 20px; height: 20px; background-color: {color}; border-radius: 3px; border: 1px solid rgba(0,0,0,0.2);"></span>
            <span style="font-weight: 600; font-size: 13px; color: #333;">{entity_type}</span>
        </div>'''
    
    legend_html += '</div>'
    return legend_html
