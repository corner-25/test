import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import numpy as np

# Cấu hình trang
st.set_page_config(
    page_title="Phân tích dữ liệu hoạt động văn phòng",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tiêu đề chính
st.title("📊 Phân tích dữ liệu hoạt động văn phòng")
st.markdown("---")

@st.cache_data
def load_sample_data():
    """Tải và xử lý dữ liệu mẫu từ file JSON đã cung cấp"""
    # Dữ liệu mẫu hoàn chỉnh từ file JSON bạn cung cấp
    sample_data = [
        {"category": "Quan ly phong hop", "content": "Tong so lich hop", "date": 6, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban phat hanh di", "content": "Tong so van ban phat hanh", "date": 7, "month": 1, "year": 2025, "count": 2},
        {"category": "Van ban den", "content": "Tong so van ban den", "date": 7, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban phat hanh hop dong", "content": "Tong so van ban phat hanh", "date": 8, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban phat hanh di", "content": "Tong so van ban phat hanh", "date": 9, "month": 1, "year": 2025, "count": 1},
        {"category": "Quan ly phong hop", "content": "Tong so lich hop", "date": 9, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban phat hanh di", "content": "Tong so van ban phat hanh", "date": 10, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban den", "content": "Tong so van ban den", "date": 13, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban phat hanh hop dong", "content": "Tong so van ban phat hanh", "date": 16, "month": 1, "year": 2025, "count": 1},
        {"category": "Quan ly phong hop", "content": "Tong so lich hop", "date": 16, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban phat hanh hop dong", "content": "Tong so van ban phat hanh", "date": 20, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban den", "content": "Tong so van ban den", "date": 20, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban den", "content": "Tong so van ban den", "date": 21, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban phat hanh quyet dinh", "content": "Tong so van ban phat hanh", "date": 21, "month": 1, "year": 2025, "count": 2},
        {"category": "Van ban phat hanh di", "content": "Tong so van ban phat hanh", "date": 21, "month": 1, "year": 2025, "count": 2},
        {"category": "Quan ly phong hop", "content": "Tong so lich hop", "date": 21, "month": 1, "year": 2025, "count": 1},
        {"category": "Van ban phat hanh di", "content": "Tong so van ban phat hanh", "date": 22, "month": 1, "year": 2025, "count": 2},
        {"category": "Van ban den", "content": "Tong so van ban den", "date": 22, "month": 1, "year": 2025, "count": 4},
        {"category": "Van ban den", "content": "Tong so van ban den", "date": 23, "month": 1, "year": 2025, "count": 4},
        {"category": "Van ban den", "content": "Tong so van ban den", "date": 24, "month": 1, "year": 2025, "count": 1},
        {"category": "Quan ly lich hop", "content": "Tong lich lam viec", "date": 3, "month": 3, "year": 2025, "count": 2},
        {"category": "Van ban phat hanh di", "content": "Tong so van ban phat hanh", "date": 4, "month": 3, "year": 2025, "count": 1},
        {"category": "Van ban phat hanh quyet dinh", "content": "Tong so van ban phat hanh", "date": 4, "month": 3, "year": 2025, "count": 1},
        {"category": "Quan ly lich hop", "content": "Tong lich lam viec", "date": 5, "month": 3, "year": 2025, "count": 4},
        {"category": "Quan ly lich hop", "content": "Tong lich lam viec", "date": 6, "month": 3, "year": 2025, "count": 178},
        {"category": "Quan ly lich hop", "content": "Tong lich lam viec", "date": 17, "month": 6, "year": 2025, "count": 862},
        {"category": "Quan ly lich hop", "content": "Tong lich lam viec", "date": 21, "month": 6, "year": 2025, "count": 243},
        {"category": "Quan ly lich hop", "content": "Tong lich lam viec", "date": 10, "month": 6, "year": 2025, "count": 151}
    ]
    
    return process_data(sample_data)

def process_data(data_list):
    """Xử lý dữ liệu chung"""
    # Chuyển đổi thành DataFrame
    df = pd.DataFrame(data_list)
    
    # Kiểm tra các cột cần thiết
    required_columns = ['category', 'date', 'month', 'year', 'count']
    if not all(col in df.columns for col in required_columns):
        st.error(f"❌ Thiếu các cột cần thiết: {[col for col in required_columns if col not in df.columns]}")
        return None
    
    # Tạo cột ngày hoàn chỉnh - SỬA CHÍNH TẠI ĐÂY
    try:
        # Rename cột 'date' thành 'day' để pandas hiểu
        df_temp = df.copy()
        df_temp['day'] = df_temp['date']  # pandas cần cột 'day' không phải 'date'
        
        df['full_date'] = pd.to_datetime(df_temp[['year', 'month', 'day']], errors='coerce')
        # Loại bỏ các dòng có ngày không hợp lệ
        df = df.dropna(subset=['full_date'])
    except Exception as e:
        st.error(f"❌ Lỗi khi tạo cột ngày: {str(e)}")
        return None
    
    # Dịch tên category sang tiếng Việt rõ ràng hơn
    category_mapping = {
        'Quan ly phong hop': 'Quản lý phòng họp',
        'Van ban phat hanh di': 'Văn bản phát hành đi',
        'Van ban den': 'Văn bản đến',
        'Van ban phat hanh hop dong': 'Văn bản hợp đồng',
        'Van ban phat hanh quyet dinh': 'Quyết định',
        'Quan ly cong viec': 'Quản lý công việc',
        'Quan ly lich hop': 'Quản lý lịch họp',
        'Van ban phat hanhquy che': 'Quy chế',
        'Van ban phat hanhhuong dan': 'Hướng dẫn',
        'Van ban phat hanhquy trinh': 'Quy trình',
        'Van ban phat hanhquy dinh': 'Quy định'
    }
    
    df['category_clean'] = df['category'].map(category_mapping).fillna(df['category'])
    
    return df

def process_uploaded_data(data):
    """Xử lý dữ liệu được upload"""
    try:
        # Kiểm tra cấu trúc dữ liệu
        if isinstance(data, dict) and 'data' in data:
            data_list = data['data']
        elif isinstance(data, list):
            data_list = data
        else:
            st.error("❌ Cấu trúc dữ liệu không hợp lệ")
            return None
        
        # Sử dụng hàm xử lý chung
        return process_data(data_list)
        
    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý dữ liệu: {str(e)}")
        return None

def create_time_series_chart(df):
    """Tạo biểu đồ thời gian"""
    # Nhóm dữ liệu theo ngày và category
    daily_data = df.groupby(['full_date', 'category_clean'])['count'].sum().reset_index()
    
    fig = px.line(
        daily_data, 
        x='full_date', 
        y='count', 
        color='category_clean',
        title='Xu hướng hoạt động theo thời gian',
        labels={'full_date': 'Ngày', 'count': 'Số lượng', 'category_clean': 'Loại hoạt động'}
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Thời gian",
        yaxis_title="Số lượng",
        legend_title="Loại hoạt động"
    )
    
    return fig

def create_category_summary(df):
    """Tạo biểu đồ tổng quan theo category"""
    category_summary = df.groupby('category_clean')['count'].sum().reset_index()
    category_summary = category_summary.sort_values('count', ascending=True)
    
    fig = px.bar(
        category_summary,
        x='count',
        y='category_clean',
        orientation='h',
        title='Tổng số lượng theo loại hoạt động',
        labels={'count': 'Tổng số lượng', 'category_clean': 'Loại hoạt động'},
        color='count',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(height=500)
    
    return fig

def create_monthly_heatmap(df):
    """Tạo heatmap theo tháng"""
    monthly_data = df.groupby(['month', 'category_clean'])['count'].sum().reset_index()
    pivot_data = monthly_data.pivot(index='category_clean', columns='month', values='count')
    pivot_data = pivot_data.fillna(0)
    
    fig = px.imshow(
        pivot_data,
        title='Phân bố hoạt động theo tháng (Heatmap)',
        labels={'x': 'Tháng', 'y': 'Loại hoạt động', 'color': 'Số lượng'},
        aspect='auto'
    )
    
    fig.update_layout(height=600)
    
    return fig

def create_daily_pattern(df):
    """Phân tích pattern theo ngày trong tháng"""
    df['day_of_month'] = df['date']
    daily_pattern = df.groupby('day_of_month')['count'].sum().reset_index()
    
    fig = px.bar(
        daily_pattern,
        x='day_of_month',
        y='count',
        title='Phân bố hoạt động theo ngày trong tháng',
        labels={'day_of_month': 'Ngày trong tháng', 'count': 'Tổng số lượng'}
    )
    
    fig.update_layout(height=400)
    
    return fig

def main():
    """Hàm chính của ứng dụng"""
    
    # Sidebar cho upload file
    st.sidebar.header("📁 Tải dữ liệu")
    uploaded_file = st.sidebar.file_uploader(
        "Chọn file JSON", 
        type=['json'],
        help="Tải lên file JSON chứa dữ liệu cần phân tích"
    )
    
    # Load dữ liệu
    df = None
    
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            df = process_uploaded_data(data)
            
            if df is not None:
                st.success(f"✅ Đã tải thành công {len(df)} bản ghi!")
            else:
                st.error("❌ Không thể xử lý dữ liệu từ file JSON")
                return
            
        except json.JSONDecodeError as e:
            st.error(f"❌ Lỗi định dạng JSON: {str(e)}")
            return
        except Exception as e:
            st.error(f"❌ Lỗi khi đọc file: {str(e)}")
            return
    else:
        # Sử dụng dữ liệu mẫu nếu không có file upload
        st.info("💡 Vui lòng tải lên file JSON để phân tích dữ liệu thực tế.")
        st.info("📊 Hiện đang hiển thị với dữ liệu mẫu.")
        df = load_sample_data()
    
    # Kiểm tra df không None
    if df is None or df.empty:
        st.error("❌ Không có dữ liệu để hiển thị")
        return
    
    # Sidebar filters
    st.sidebar.header("🔧 Bộ lọc")
    
    # Filter theo category
    categories = df['category_clean'].unique()
    selected_categories = st.sidebar.multiselect(
        "Chọn loại hoạt động:",
        categories,
        default=categories
    )
    
    # Filter theo thời gian
    date_range = st.sidebar.date_input(
        "Chọn khoảng thời gian:",
        value=[df['full_date'].min().date(), df['full_date'].max().date()],
        min_value=df['full_date'].min().date(),
        max_value=df['full_date'].max().date()
    )
    
    # Áp dụng filter
    if len(date_range) == 2:
        mask = (
            (df['category_clean'].isin(selected_categories)) &
            (df['full_date'].dt.date >= date_range[0]) &
            (df['full_date'].dt.date <= date_range[1])
        )
        filtered_df = df[mask]
    else:
        filtered_df = df[df['category_clean'].isin(selected_categories)]
    
    # Hiển thị thống kê tổng quan
    st.header("📈 Thống kê tổng quan")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(filtered_df)
        st.metric("Tổng số bản ghi", f"{total_records:,}")
    
    with col2:
        total_count = filtered_df['count'].sum()
        st.metric("Tổng số lượng", f"{total_count:,}")
    
    with col3:
        avg_count = filtered_df['count'].mean()
        st.metric("Trung bình/ngày", f"{avg_count:.1f}")
    
    with col4:
        unique_categories = filtered_df['category_clean'].nunique()
        st.metric("Số loại hoạt động", unique_categories)
    
    # Tab layout cho các biểu đồ
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Tổng quan", 
        "📈 Xu hướng thời gian", 
        "🔥 Heatmap", 
        "📅 Theo ngày", 
        "📋 Dữ liệu chi tiết"
    ])
    
    with tab1:
        st.plotly_chart(create_category_summary(filtered_df), use_container_width=True)
        
        # Top 5 ngày có hoạt động cao nhất
        st.subheader("🔝 Top 5 ngày có hoạt động cao nhất")
        top_days = filtered_df.groupby('full_date')['count'].sum().nlargest(5)
        for date, count in top_days.items():
            st.write(f"📅 **{date.strftime('%d/%m/%Y')}**: {count} hoạt động")
    
    with tab2:
        st.plotly_chart(create_time_series_chart(filtered_df), use_container_width=True)
    
    with tab3:
        st.plotly_chart(create_monthly_heatmap(filtered_df), use_container_width=True)
    
    with tab4:
        st.plotly_chart(create_daily_pattern(filtered_df), use_container_width=True)
    
    with tab5:
        st.subheader("📋 Dữ liệu chi tiết")
        
        # Hiển thị bảng với khả năng sort
        display_df = filtered_df[['full_date', 'category_clean', 'content', 'count']].copy()
        display_df['full_date'] = display_df['full_date'].dt.strftime('%d/%m/%Y')
        display_df.columns = ['Ngày', 'Loại hoạt động', 'Nội dung', 'Số lượng']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
        
        # Nút download
        csv = filtered_df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="📥 Tải xuống dữ liệu CSV",
            data=csv,
            file_name=f"data_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()