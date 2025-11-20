import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Research Dashboard | NIT Jalandhar", 
                   page_icon="📊", 
                   layout="wide")

# ---------- TITLE ----------
st.title("🏠 Research Overview Dashboard")
st.markdown("### A summary of NIT Jalandhar’s Research Performance and Collaborations")

st.divider()

# ---------- SAMPLE DATA ----------
# (Replace with your own data sources or CSV)

df = pd.read_csv("Data/h-index.csv")




departments = df['Category']
publications = df['Publications']
citations = df['Citations']
years = list(range(2015, 2025))
pubs_by_year = [40, 55, 68, 72, 90, 105, 115, 130, 142, 160]
types = ["Journal", "Conference", "Book Chapter", "Workshop"]
type_counts = [250, 180, 40, 20]
hIndex = df['h-index']

# ---------- KPI CARDS ----------
# col1, col2, col3, col4, col5 = st.columns(5)
# col1.metric("📚 Total Publications", "895", "+12%")
# col2.metric("🧾 Total Citations", "8,250", "+9%")
# col3.metric("📈 Average H-index", "28.4", "+5%")
# col4.metric("🔬 Top Research Area", "AI & IoT")
# col5.metric("🤝 Active Collaborations", "32", "+7%")


metrics = {
    "📚 Total Publications": int(publications.sum()),
    "🧾 Total Citations": int(citations.sum()),
    "📈 Average H-index": hIndex.mean(),  # float value
    "🔬 Top Research Area": "AI & IoT",
    "🤝 Active Collaborations": 32
}



# ---------- CSS ----------
image_map = {
    "📚 Total Publications": "https://images.unsplash.com/photo-1512820790803-83ca734da794",
    "🧾 Total Citations": "https://www.shutterstock.com/image-vector/luxury-gold-text-quote-symbol-600nw-2244631733.jpg",
    "📈 Average H-index": "https://scientific-publishing.webshop.elsevier.com/wp-content/uploads/2020/04/What-is-a-good-index.jpg",
    "🔬 Top Research Area": "https://media.istockphoto.com/id/861104740/vector/health-care-icon-pattern-medical-innovation-concept-background-design.jpg?s=612x612&w=0&k=20&c=2T7h9lyPZLtrjmFn1xAfqxvziavz7520ML7UKlx5RhE=",
    "🤝 Active Collaborations": "https://images.unsplash.com/photo-1507537297725-24a1c029d3ca"
}

# ---------- CSS ----------
st.markdown("""
<style>
.card {
    border-radius: 16px;
    box-shadow: 2px 6px 12px rgba(0,0,0,0.15);
    padding: 20px;
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
    color: #fff;
    position: relative;
    overflow: hidden;
    perspective: 1000px;
}
.card:hover {
    transform: rotateY(10deg) rotateX(5deg) scale(1.05);
    box-shadow: 2px 8px 16px rgba(0,0,0,0.25);
}

/* Shiny overlay that follows mouse */
.card::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 200%; height: 200%;
    pointer-events: none;
    background: radial-gradient(circle 150px at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(255,255,255,0.4), transparent 40%);
    transform: translate(-50%, -50%);
    transition: background 0.1s;
}
.metric-title { font-size: 18px; font-weight: 500; margin-bottom: 10px; }
.metric-value { font-size: 36px; font-weight: bold; }
</style>

<script>
const cards = document.querySelectorAll('.card');
cards.forEach(card => {
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        card.style.setProperty('--mouse-x', x + '%');
        card.style.setProperty('--mouse-y', y + '%');
    });
});
</script>
""", unsafe_allow_html=True)

# ---------- Layout ----------
cols = st.columns(5)
metric_containers = []

for col, (title, value) in zip(cols, metrics.items()):
    with col:
        container = st.empty()
        metric_containers.append((container, title, value))

# ---------- Animate Numbers ----------
for container, title, value in metric_containers:
    bg_image = image_map[title]
    if isinstance(value, int):
        displayed = 0
        step = max(1, value // 50)
        while displayed < value:
            displayed += step
            if displayed > value: displayed = value
            container.markdown(f"""
                <div class="card" style="
                    background-image: url('{bg_image}');
                    background-size: cover;
                    background-position: center;">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{displayed:,}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.02)
    elif isinstance(value, float):
        displayed = 0.0
        step = max(0.01, value / 50)
        while displayed < value:
            displayed += step
            if displayed > value: displayed = value
            container.markdown(f"""
                <div class="card" style="
                    background-image: url('{bg_image}');
                    background-size: cover;
                    background-position: center;">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{displayed:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.02)
    else:
        container.markdown(f"""
            <div class="card" style="
                background-image: url('{bg_image}');
                background-size: cover;
                background-position: center;">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)





st.divider()

# ---------- CHARTS SECTION ----------
st.subheader("📊 Research Trends & Department Insights")

# Split layout
# col1, col2 = st.columns((2, 2))

# Bar Chart: Publications per Department
bar_fig = px.bar(
    x=departments, y=publications,
    labels={"x": "Department", "y": "Number of Publications"},
    title="Publications per Department",
    color=departments,
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(bar_fig, use_container_width=True)

# Line Chart: Publications by Year
line_fig = px.line(
    x=years, y=pubs_by_year,
    markers=True,
    labels={"x": "Year", "y": "Publications"},
    title="Publications by Year"
)
st.plotly_chart(line_fig, use_container_width=True)

st.divider()

# ---------- PIE CHART ----------
st.subheader("📚 Distribution by Publication Type")
pie_fig = px.pie(
    names=types, values=type_counts,
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.RdBu,
)
pie_fig.update_traces(textposition="inside", textinfo="percent+label")
st.plotly_chart(pie_fig, use_container_width=True)

st.divider()

# ---------- MAP VISUAL ----------
st.subheader("🗺️ Research Collaborations & Conference Locations")

map_data = pd.DataFrame({
    'lat': [31.3959, 28.6139, 19.0760, 35.6895, 51.5074, 40.7128],
    'lon': [75.5358, 77.2090, 72.8777, 139.6917, -0.1278, -74.0060],
    'location': ['NIT Jalandhar', 'Delhi', 'Mumbai', 'Tokyo', 'London', 'New York']
})

map_fig = px.scatter_geo(
    map_data,
    lat='lat', lon='lon',
    hover_name='location',
    title='Global Collaboration Map',
    projection="natural earth"
)
st.plotly_chart(map_fig, use_container_width=True)

st.divider()
st.caption("© 2025 NIT Jalandhar | Developed for Data Visualization Course Project")
