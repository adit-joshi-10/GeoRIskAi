import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# GLOBAL TAB
# =====================================================

def render_global_tab(

    filtered_df,

    PLOTLY_LAYOUT
):

    col_map, col_alerts = st.columns([2, 1])

    # =================================================
    # MAP SECTION
    # =================================================

    with col_map:

        st.markdown(
            '''
            <div class="section-label">
            Threat Assessment
            </div>

            <div class="section-title">
            Global Risk Globe
            </div>
            ''',
            unsafe_allow_html=True
        )

            # =================================================
    # MAP SECTION
    # =================================================

    with col_map:

        st.markdown(
            '''
            <div class="section-label">
            Threat Assessment
            </div>

            <div class="section-title">
            Global Risk Globe
            </div>
            ''',
            unsafe_allow_html=True
        )

        # =============================================
        # COUNTRY COORDINATES
        # =============================================

        country_coords = {

            "United States": [37.0902, -95.7129],
            "Russia": [61.5240, 105.3188],
            "China": [35.8617, 104.1954],
            "India": [20.5937, 78.9629],
            "Iran": [32.4279, 53.6880],
            "Israel": [31.0461, 34.8516],
            "Ukraine": [48.3794, 31.1656],
            "Pakistan": [30.3753, 69.3451],
            "North Korea": [40.3399, 127.5101],
            "South Korea": [35.9078, 127.7669],
            "Afghanistan": [33.9391, 67.7100],
            "Syria": [34.8021, 38.9968],
            "Venezuela": [6.4238, -66.5897],
            "Taiwan": [23.6978, 120.9605],
        }

        filtered_df["Latitude"] = filtered_df[
            "Country"
        ].map(
            lambda x:
            country_coords.get(x, [0,0])[0]
        )

        filtered_df["Longitude"] = filtered_df[
            "Country"
        ].map(
            lambda x:
            country_coords.get(x, [0,0])[1]
        )

        # =============================================
        # HOVER TEMPLATE
        # =============================================

        hover_template = (

            "<b style='font-size:13px'>"
            "%{customdata[0]}"
            "</b><br>"

            "<span style='color:#3a6070'>"
            "━━━━━━━━━━━━━━━━━━"
            "</span><br>"

            "GeoRisk Score &nbsp; "
            "<b style='color:#00e5ff'>"
            "%{marker.color:.4f}"
            "</b><br>"

            "Risk Level &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
            "<b>%{customdata[1]}</b><br>"

            "Conflict Prob &nbsp; "
            "<b style='color:#ff9500'>"
            "%{customdata[2]:.4f}"
            "</b><br>"

            "News Risk &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
            "<b style='color:#ff3b5c'>"
            "%{customdata[3]:.4f}"
            "</b><br>"

            "<extra></extra>"
        )

        # =============================================
        # INTERACTIVE 3D GLOBE
        # =============================================

        map_fig = go.Figure()

        map_fig.add_trace(

            go.Scattergeo(

                lon=filtered_df["Longitude"],

                lat=filtered_df["Latitude"],

                text=filtered_df["Country"],

                customdata=filtered_df[
                    [
                        "Country",
                        "Dynamic_Risk_Level",
                        "Conflict_Probability",
                        "News_Risk_Score"
                    ]
                ].values,

                hovertemplate=hover_template,

                mode="markers",

                marker=dict(

                    size=(
                        filtered_df[
                            "GeoRisk_Live_Score"
                        ] * 35
                    ),

                    color=filtered_df[
                        "GeoRisk_Live_Score"
                    ],

                    colorscale=[

                        [0.00, "#00e5ff"],

                        [0.35, "#00ffaa"],

                        [0.60, "#ffaa00"],

                        [0.80, "#ff5c00"],

                        [1.00, "#ff1a3c"],
                    ],

                    opacity=0.95,

                    line=dict(
                        width=1.2,
                        color="#ffffff"
                    ),
                ),
            )
        )

        # =============================================
        # GLOBE LAYOUT
        # =============================================

        map_fig.update_layout(

            height=720,

            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0
            ),

            paper_bgcolor="#020609",

            geo=dict(

                projection_type="orthographic",

                bgcolor="#020609",

                showocean=True,
                oceancolor="#020d18",

                showland=True,
                landcolor="#071420",

                showlakes=True,
                lakecolor="#020d18",

                showcountries=True,
                countrycolor="#16354d",

                showcoastlines=True,
                coastlinecolor="#16354d",

                showframe=False,

                lataxis=dict(
                    showgrid=False
                ),

                lonaxis=dict(
                    showgrid=False
                ),

                projection_rotation=dict(

                    lon=20,
                    lat=10,
                    roll=0
                )
            )
        )

        st.plotly_chart(
            map_fig,
            use_container_width=True
        )
                # =============================================
        # TOP THREATS CHART
        # =============================================

        st.markdown(
            '''
            <div class="section-label">
            Top Threats
            </div>

            <div class="section-title">
            Highest Risk Countries
            </div>
            ''',
            unsafe_allow_html=True
        )

        top10 = filtered_df.nlargest(
            10,
            "GeoRisk_Live_Score"
        )

        bar_fig = px.bar(

            top10,

            x="Country",

            y="GeoRisk_Live_Score",

            color="Dynamic_Risk_Level",

            color_discrete_map={

                "Critical":"#ff3b5c",

                "High":"#ff9500",

                "Medium":"#ffe600",

                "Low":"#00ff88"
            },

            text="GeoRisk_Live_Score",
        )

        bar_fig.update_layout(

            **PLOTLY_LAYOUT,

            height=320,

            bargap=0.35
        )

        st.plotly_chart(

            bar_fig,

            use_container_width=True
        )
            # =================================================
    # ALERTS PANEL
    # =================================================

    with col_alerts:

        st.markdown(
            '''
            <div class="section-label">
            Intelligence Feed
            </div>

            <div class="section-title">
            Strategic Alerts
            </div>
            ''',
            unsafe_allow_html=True
        )

        top_alerts = filtered_df.nlargest(
            6,
            "GeoRisk_Live_Score"
        )

        for _, row in top_alerts.iterrows():

            country = row["Country"]

            score = row[
                "GeoRisk_Live_Score"
            ]

            risk = row[
                "Dynamic_Risk_Level"
            ]

            news = row[
                "News_Risk_Score"
            ]

            if risk == "Critical":

                color = "#ff3b5c"

                icon = "🔴"

            elif risk == "High":

                color = "#ff9500"

                icon = "🟠"

            elif risk == "Medium":

                color = "#ffe600"

                icon = "🟡"

            else:

                color = "#00ff88"

                icon = "🟢"

            st.markdown(

                f"""
<div style="
background:rgba(5,15,25,0.95);
border:1px solid {color};
border-radius:14px;
padding:14px;
margin-bottom:12px;
box-shadow:0 0 18px rgba(0,0,0,0.35);
">

<div style="
font-size:0.75rem;
color:{color};
font-family:'Share Tech Mono',monospace;
letter-spacing:0.08em;
margin-bottom:6px;
">

{icon} {risk.upper()} ALERT

</div>

<div style="
font-size:1rem;
font-weight:700;
color:white;
margin-bottom:8px;
">

{country}

</div>

<div style="
display:flex;
justify-content:space-between;
font-size:0.8rem;
color:#9db4c0;
">

<span>
GeoRisk: <b>{score:.2f}</b>
</span>

<span>
News: <b>{news:.2f}</b>
</span>

</div>

</div>
                """,

                unsafe_allow_html=True
            )

        st.markdown("---")

        st.caption(
            "Live geopolitical intelligence "
            "monitoring active."
        )