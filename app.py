import math
import streamlit as st

# 1. 웹사이트의 기본 설정
st.set_page_config(
    page_title="학교 축제 부스 수익 계산기",
    page_icon="🏫",
    layout="centered"
)

# 2. 제목과 소개
st.title("🏫 학교 축제 부스 수익 계산기")
st.write(
    "판매가격과 비용을 입력하고, "
    "우리 부스가 얼마나 이익을 낼 수 있는지 확인해 보세요!"
)

st.info(
    "제품 1개당 재료비에는 포장비 등 "
    "판매 수량에 따라 늘어나는 비용도 포함해 주세요."
)

# 3. 사용자가 값을 입력하는 부분
with st.form("profit_form"):
    product = st.text_input(
        "판매할 상품 이름",
        value="쿠키"
    )

    price = st.number_input(
        "제품 1개 판매가격 (원)",
        min_value=0,
        value=3000,
        step=100
    )

    unit_cost = st.number_input(
        "제품 1개당 재료비·포장비 (원)",
        min_value=0,
        value=1200,
        step=100
    )

    quantity = st.number_input(
        "예상 판매량 (개)",
        min_value=0,
        value=100,
        step=1
    )

    fixed_cost = st.number_input(
        "부스 운영비 (원)",
        min_value=0,
        value=50000,
        step=1000,
        help="장식비, 장비 대여비 등 판매량과 관계없이 드는 비용"
    )

    submitted = st.form_submit_button("예상 수익 계산하기")

# 4. 계산 버튼을 눌렀을 때 실행
if submitted:
    sales = price * quantity
    variable_cost = unit_cost * quantity
    total_cost = variable_cost + fixed_cost
    profit = sales - total_cost
    unit_margin = price - unit_cost

    st.divider()
    st.subheader(f"📊 {product or '상품'} 부스의 예상 결과")

    st.metric("예상 매출", f"{sales:,}원")
    st.metric("예상 총비용", f"{total_cost:,}원")
    st.metric("예상 이익", f"{profit:,}원")

    # 이익에 따른 안내
    if profit > 0:
        st.success(f"예상 이익은 {profit:,}원입니다!")
    elif profit == 0:
        st.info("예상 매출과 총비용이 같아 이익은 0원입니다.")
    else:
        st.error(f"예상 손실은 {-profit:,}원입니다.")

    # 5. 손익분기 판매량 계산
    st.subheader("🎯 얼마나 팔아야 적자를 벗어날까요?")

    if unit_margin > 0:
        break_even = math.ceil(fixed_cost / unit_margin)

        st.write(
            f"제품 1개를 팔 때 고정비 회수와 이익에 "
            f"보탤 수 있는 금액은 **{unit_margin:,}원**입니다."
        )

        st.info(
            f"적자를 벗어나기 위한 최소 판매량은 "
            f"**{break_even:,}개**입니다."
        )

        if quantity < break_even:
            extra = break_even - quantity
            st.warning(
                f"현재 예상 판매량보다 {extra:,}개를 더 팔아야 합니다."
            )
        else:
            st.success("예상 판매량이 손익분기 판매량 이상입니다.")

    elif unit_margin == 0:
        if fixed_cost > 0:
            st.warning(
                "판매가격과 개당 재료비가 같아 "
                "아무리 많이 팔아도 부스 운영비를 회수할 수 없습니다."
            )
        else:
            st.info(
                "판매가격과 개당 재료비가 같고 운영비가 0원이므로 "
                "판매량에 관계없이 이익은 0원입니다."
            )

    else:
        st.warning(
            "판매가격이 개당 재료비보다 낮아 "
            "판매할수록 손실이 커집니다. 가격이나 비용을 조정해 보세요."
        )

    # 6. 계산 과정 설명
    with st.expander("계산 과정 자세히 보기"):
        st.write(
            f"매출 = {price:,}원 × {quantity:,}개 "
            f"= {sales:,}원"
        )
        st.write(
            f"총비용 = {unit_cost:,}원 × {quantity:,}개 "
            f"+ {fixed_cost:,}원 = {total_cost:,}원"
        )
        st.write(
            f"이익 = {sales:,}원 - {total_cost:,}원 "
            f"= {profit:,}원"
        )

st.divider()
st.caption(
    "계산 가정: 생산한 제품은 모두 판매하며, "
    "개당 비용과 판매가격은 일정하다고 가정합니다."
)
