# ============================================================
# VELLA V6 — app.py
# ============================================================

# ============================================================
# [ER-CFG-000] CFG ROOT OBJECT (튜닝 공간)
# ============================================================

CFG = {

    # =====================================================
    # [PRIORITY 0] 자본·종목 (가장 중요 / AWS에서 자주 만짐)
    # =====================================================
    "0_TRADE_SYMBOL": "WOOUSDT.P",
    # [설명] 거래 종목. ".P"는 선물(FUTURES) 표시 태그(표시용)
    "0_CAPITAL_BASE_USDT": 60,
    # [설명] 기준 투자금(USDT). 포지션 사이즈 계산의 기준이 되는 값.
    "0_CAPITAL_USE_FIXED": True,
    # [설명] True면 항상 위 USDT를 고정 사용. # [추천] True 고정.
    # [사유] 잔고변동 포지션 흔들리면 전략 성능, 자본변동이 섞여 분석 깨짐.
    "0_CAPITAL_MAX_LOSS_PCT": 100.0,
    # [설명] 엔진 레벨 최대 손실 허용(%) — 100이면 전액 손실 허용.
    # [추천] 실험: 100 / 실가동 확대 시: 10~30 고려(방어 강화).
    # [사유] 지금은 실전 작동 확인/데이터 확보가 목표
    # =====================================================
    # [PRIORITY 1] 엔진 ON/OFF (운영 스위치)
    # =====================================================
    "1_ENGINE_ENABLE": True,
    # [설명] 엔진 마스터 스위치.  # [추천]긴급중단/점검 시 False.
    # [사유] systemd는 계속 살려두고 “거래만” 즉시 멈추는 레버.
    "2_ENTRY_CANDIDATE_ENABLE": True,
    # [설명] 후보 등록 ON/OFF.  # [추천]원칙 True 유지(후보 넓게).
    # [사유] 차단은 후단(쿨다운/재진입)에서.
    "3_ENTRY_EXEC_ENABLE": True,
    # [설명] 후보가 있어도 실제 주문 허용할지.
    # [추천] 디버그/검증만 할 땐 False, 실가동은 True.
    # [사유] “후보 로그는 쌓되 주문은 막기”가 가능한 안전 레버.
    # =====================================================
    # [PRIORITY 2] 후보 조건(단순 / 똑똑하게 만들지 않는다)
    # =====================================================
    "4_EMA_PERIOD": 9,
    # [설명] EMA 기간. 후보 판정의 기준선.
    # [추천] 9 고정(기본). 필요 시 7(민감/진입↑) ~ 14(둔감/진입↓).
    # [사유] 기간이 짧을수록 EMA가 가격을 더 “따라붙어” 후보가 더 자주 생김.
    "5_CAND_BODY_BELOW_EMA": True,
    # [설명] True면 “봉 몸통 하단(body_low)이 EMA 아래면 후보”.
    # [추천] True 고정.  # [사유] 후보를 넓게 잡는 핵심 스위치.
    "6_CAND_USE_CLOSE_ONLY": False,
    # [설명] True면 후보 판정에 종가(close)만 쓰는 식으로 단순화(정보 감소).
    # [추천] False(기본). True는 후보를 줄이고 싶을 때만.
    # [사유] close는 노이즈 줄이지만, 반대로 진입이 늦을수 있다.
    # =====================================================
    # [PRIORITY 3] 연타·쿨다운(횡보 대응 핵심은 "진입 차단"이 아니라 "연타 차단")
    # =====================================================
    "7_ENTRY_COOLDOWN_BARS": 1,
    # [설명] 마지막 엔트리 이후 최소 대기 봉 수.
    # [추천] 1~3: # - 1= 공격적(진입↑, 연타↑), - 3 = 보수적(진입↓, 연타↓)
    # [사유] 횡보 구간에서 “연속 진입 폭주”를 막는 1번 레버.
    "8_ENTRY_COOLDOWN_AFTER_EXIT": 0,
    # [설명] 청산 직후 재진입까지 최소 대기 봉 수.
    # [추천] 0~2: # - 0 = 공격적(바로재진입,진입↑/휩쏘, # - 2 = 보수적(재진입↓ / 휩쏘↓)
    # =====================================================
    # [PRIORITY 4] 재진입 차단(반복 vs 새정보 프레임)
    # =====================================================
    "9_REENTRY_SAME_REASON_BLOCK": True,
    # [설명] 같은 이유(reason)로 반복 진입을 막을지.
    # [추천] True 고정. # [사유] “반복을 억제, 새정보 다른 reason으로 들어오게 설계.
    "10_ENTRY_LOOKBACK_BARS": 2,
    # [설명] 과거 N봉을 보며 “최근에 비슷한 진입이 있었나” 판단하는 범위.
    # [추천] 3~8: # - 3 = 공격적(과거덜봄→재진입↑), - 8= 보수적(과거를 더 봄 → 재진입↓)
    # [사유] lookback이 길수록 “반복” 판정을 더 자주 하게 됨(연타 억제 강화).
    "11_REENTRY_PRICE_TOL_PCT": 0.05,
    # [설명] “같은 자리” 간주하는 가격 허용오차(%), 작을수록 엄격, 클수록 같은 자리로 봄.
    # [추천] 0.05~0.30: # - 0.05 = 공격적(같은 자리 판정 ↓ → 재진입↑)
    #   - 0.30 = 보수적(같은 자리 판정 ↑ → 재진입↓)
    # [사유] 횡보에서 가격이 살짝만 움직여도 계속 진입하는 것을 막는 레버.
    # =====================================================
    # [PRIORITY 5] 횡보제어, 상태 기반 제어(STATE 라벨은 "판단"이 아니라 "라벨" / 사용 여부는 CFG)
    # =====================================================
    "12_STATE_COOLDOWN_ENABLE": False,
    # [설명] RANGE/TREND 라벨을 이용해 쿨다운을 다르게 줄지.
    # [추천] True(기본). False는 단순 운용.
    # [사유] 횡보(RANGE)에서만 강하게 연타 차단, 추세(TREND)에서는 기회 유지가 핵심.
    "13_COOLDOWN_RANGE_BARS": 0,
    # [설명] 시장 상태가 RANGE일 때 적용되는 엔트리 쿨다운(봉 수).
    # [추천] 3~7: # - 3= 공격적(횡보진입 더함), -7 = 보수적(횡보 진입 크게 줄임)
    # [사유] “횡보 대응 = 진입 차단”이 아니라 “연타 차단”의 대표 레버.
    "14_COOLDOWN_TREND_BARS": 0,
    # [설명] 시장 상태가 TREND일 때 적용되는 엔트리 쿨다운.
    # [추천] 0~2: # - 0= 공격적(추세 재진입↑), - 2= 보수적(추세에서도 진입↓)
    # [사유] 추세는 기회 구간이므로 RANGE보다 쿨다운을 짧게 두는 게 원칙.
    # =====================================================
    # [PRIORITY 6] 후보 풀(후보를 넓게 잡되, "오래된 후보"는 폐기)
    # =====================================================
    "15_CAND_POOL_TTL_BARS": 8,
    # [설명] 후보가 생성된 뒤 최대 몇 봉까지 유효한지(TTL).
    # [추천] 4~8: # - 4= 공격적(신선도 엄격 → 후보 빨리 폐기)
    # - 8 = 보수적(후보 오래 유지 → 실행 기회↑)
    # [사유] 너무 오래된 후보는 “새 정보”가 아니라 “과거 흔적”오판 가능.
    "16_CAND_POOL_MAX_SIZE": 3,
    # [설명] 동시에 유지할 후보 최대 개수. # [추천] 1~5:
    # - 1= 보수적(가장 강한 후보만), - 5 = 공격적(후보 많이 쌓음 → 실행 기회↑/ 관리 복잡↑)
    # [사유] 후보를 너무 많이 쌓으면 “후보 과잉→연타”로 연결될 수 있음.
    "17_CAND_MIN_GAP_BARS": 1,
    # [설명] 후보 생성 간 최소 간격(봉).
    # [추천] 0~2: # - 0= 공격적(후보 매우 자주), - 2 = 보수적(후보 빈도↓)
    # [사유] 후보 단계에서도 과도한 중복 생성을 막는 완충재.
    # =====================================================
    # [PRIORITY 7] 안전장치(폭주/데이터 이상 차단)
    # =====================================================
    "18_ENTRY_MAX_PER_CYCLE": 1,
    # [설명] 1 사이클(엔진 정의 기준)에서 허용하는 최대 엔트리 횟수.
    # [추천] 1 고정.  # [사유] “딱 1번 실행” 원칙을 강제(폭주 방지).
    "19_MAX_ENTRIES_PER_DAY": 20,
    # [설명] 하루 최대 엔트리 횟수 상한. # [추천] 실험: 20~50 / 보수 운영: 5~15.
    # [사유] 비정상 폭주(버그/시장 이상) 시 손실을 ‘상한’으로 막는 마지막 울타리.
    "20_DATA_STALE_BLOCK": True,
    # [설명] 데이터가 오래되면 엔트리 차단할지.
    # [추천] True 고정 # [사유] False 진입 “엉뚱한 가격”에 주문 위험(운영 안전).
    # =====================================================
    # [PRIORITY 8] 변동성 필터(선택: 데이터 확보 후 켜도 됨)
    # =====================================================
    "21_VOLATILITY_BLOCK_ENABLE": False,
    # [설명] 변동성이 너무 크면 엔트리를 차단할지.
    # [추천] 초기: False(진입 데이터 확보) / 안정화 후: True 고려.
    # [사유] 처음부터 차단하면 “왜 안 들어갔는지” 데이터가 부족해 튜닝이 느려짐.
    "22_VOLATILITY_MAX_PCT": 2.5,
    # [설명] 변동성 상한(%) — 초과 시 엔트리 차단(Enable일 때만).
    # [추천] 1.5~4.0: # - 1.5= 보수(급변 대부분 차단), 
    # - 4.0 = 공격적(급변에서도 진입 허용)
    # [사유] 급변 구간은 체결/슬리피지/휩쏘 커서, 안정화 차단이 유리.
    # =====================================================
    # [PRIORITY 9] 로그·디버그(실전 검증용)
    # =====================================================
    "23_LOG_CANDIDATES": True,
    # [설명] 후보 등록 로그 기록.  # [추천] True(최소한 이건 켜고 간다).
    # [사유] “왜 후보가 생겼는지/안 생겼는지”가 튜닝의 출발점.
    "24_LOG_EXECUTIONS": True,
    # [설명] 주문 실행/체결 결과 로그 기록.
    # [추천] True 고정. # [사유] 실전 검증의 단일 진실(체결 데이터)이기 때문.
    "25_DEBUG_LABEL_ENABLE": False,
    # [설명] 디버그 라벨(시각화/추적용) 사용 여부.
    # [추천] 운영: False / 디버그 세션: True.
    # [사유] 운영 중에는 불필요한 출력/부하를 줄여 안정성 최우선.

# =====================================================
# [PRIORITY 10] BTC REGIME FILTER (V6 NEW)
# 목적: 알트 엔트리 허용/차단을 BTC 상태로 “완화 제어”
# =====================================================

"26_BTC_REGIME_ENABLE": False,
# [설명] BTC 레짐 필터 사용 여부
# False: BTC 완전 무시 (v4/v5 동일)
# True : 아래 MODE 기준으로 부분 제어

"27_BTC_REGIME_MODE": "PULSE",
# [설명] BTC 레짐 동작 모드
# "PULSE"  : 단기 조건 충족 시에만 허용(완화형, v6 기본)
# "STRICT" : 조건 불충족 시 전면 차단(비권장)
# "OFF"    : ENABLE=False와 동일

"28_BTC_TIMEFRAME": "5m",
# [설명] BTC 기준 타임프레임
# [권장] 5m (알트 엔트리 타이밍과 동기)

"29_BTC_PULSE_LOOKBACK_BARS": 3,
# [설명] 최근 N봉 내 BTC 상태 확인 범위
# [권장] 2~5 (작을수록 공격적)

"30_BTC_PULSE_MIN_MOVE_PCT": 0.15,
# [설명] 최근 N봉 동안 BTC 최소 변동폭(%)
# [권장] 0.10 ~ 0.30
# [사유] BTC가 ‘살아있는 장’인지 판별

"31_BTC_BLOCK_ON_SHARP_DROP": True,
# [설명] BTC 급락 시 알트 엔트리 차단 여부

"32_BTC_SHARP_DROP_PCT": -0.40,
# [설명] BTC 단봉 급락 기준(%)
# 예: -0.40 = 5m 기준 -0.4% 급락 시 차단

"33_BTC_PULSE_TTL_BARS": 3,
# [설명] BTC 펄스 허용 상태 유지 봉 수
# [권장] 2~4
# [사유] BTC 조건이 잠깐 충족돼도 알트가 따라올 시간 확보

}

# ============================================================
# [ENGINE_RULE] CFG ACCESS FUNCTIONS
# ============================================================

# ============================================================
# [ER-CFG-011] GET TRADE SYMBOL CONTRACT
# ============================================================
def get_trade_symbol(cfg: dict) -> str:
    symbol = cfg.get("0_TRADE_SYMBOL", "").strip()
    if not symbol:
        raise RuntimeError("CFG ERROR: 0_TRADE_SYMBOL is empty")
    return symbol

# ============================================================
# [ER-CFG-012] GET CAPITAL BASE CONTRACT
# ============================================================
def get_capital_base(cfg: dict) -> float:
    return float(cfg["0_CAPITAL_BASE_USDT"])

# ============================================================
# VELLA V4 — ENGINE_RULE ID CATALOG (v0.2 / LOG-ONLY EXTENDED)
# ============================================================
# [ER-SYM] SYMBOL_RESOLVER
ER_ID = {
    "ER-SYM-001": "symbol_info는 SYMBOL_RESOLVER 1곳에서만 생성된다 (Single Source of Truth).",
    "ER-SYM-002": "API 호출에는 반드시 symbol_info.base만 사용한다.",
    "ER-SYM-003": "market 타입(예: FUTURES)은 symbol_info.market에서만 온다.",
    "ER-SYM-004": "CFG의 0_TRADE_SYMBOL이 비었으면 엔진은 즉시 예외로 차단한다.",

    # [ER-CFG] CFG_MANAGER / CONTRACT
    "ER-CFG-001": "CFG는 의미 해석을 하지 않는다. 엔진이 CFG 값을 그대로 소비한다.",
    "ER-CFG-002": "전략/강도/필터는 CFG 조합으로만 바뀐다 (엔진 불변).",

    # [ER-FEED] DATA_FEED
    "ER-FEED-010": "CandleBuffer가 완료봉/진행중봉 단일 진실이다.",
    "ER-FEED-011": "DataFeed 내부 버퍼 키는 symbol_info.base로 통일한다.",
    "ER-FEED-012": "REST 스냅샷 후 WS/폴링 갱신 인터페이스는 동일해야 한다.",
    "ER-FEED-013": "stale 판정은 DataFeed의 last_update_ms 기준으로만 한다.",

    # [ER-IND] INDICATOR_MODULE
    "ER-IND-001": "지표 계산은 완료봉 기준이 기본이며, 진행중봉 사용 여부는 CFG로만 제어한다.",

    # [ER-ENTRY] ENTRY ENGINE RULE
    "ER-ENTRY-001": "후보는 넓게 등록하고, 선별/차단은 후단 필터에서만 한다.",
    "ER-ENTRY-002": "연타(횡보) 대응은 후보 차단이 아니라 재진입/쿨다운 제어로 한다.",
    "ER-ENTRY-003": "필터/차단 기준은 전부 CFG로만 튜닝 가능해야 한다.",

    # [ER-EXEC] EXECUTION_MODULE
    "ER-EXEC-020": "주문 실행은 판단 금지. 요청을 전달하고 결과만 표준화해 반환한다.",
    "ER-EXEC-021": "create_order는 symbol=symbol_info.base, market=symbol_info.market 계약을 따른다.",
    "ER-EXEC-022": "재시도/타임아웃은 EXEC_CFG로만 제어한다 (전략값 사용 금지).",

    # [ER-REC] RECONCILER
    "ER-REC-030": "reconcile의 조회/비교는 반드시 symbol_info.base 기준으로 수행한다.",
    "ER-REC-031": "mismatch 조치는 CFG 정책(HALT/STATE_FIX/FORCE_EXIT)으로만 결정한다.",
    "ER-REC-032": "FORCE_EXIT는 reduce-only로만 시도하며, 실패 시 정책대로 HALT/보고한다.",

    # ========================================================
    # [ER-STATE] STATE_MODULE (LABELER ONLY)  ★ 추가
    # ========================================================
    "ER-STATE-001": "STATE_MODULE은 판단하지 않고 시장 상태를 라벨로만 제공한다.",
    "ER-STATE-002": "STATE_MODULE 출력은 고정 라벨 집합만 허용한다 (예: RANGE, TREND).",
    "ER-STATE-003": "상태 라벨의 의미/강도/사용 여부는 CFG로만 결정한다.",
    "ER-STATE-004": "STATE_MODULE은 엔트리·청산·주문 로직에 직접 관여하지 않는다.",

    # ========================================================
    # [ER-LOG] LOG / TELEMETRY — WRITE ONLY EXTENSION
    # (모듈 추가 없음 / 판단·피드백 금지 / 기록 전용)
    # ========================================================
    "ER-LOG-001":  "LOG는 엔진 판단과 완전히 분리된 기록 전용 영역이다.",
    "ER-LOG-001.a": "이벤트/후보/필터/상태 변화는 WRITE-ONLY로 기록한다.",
    "ER-LOG-001.b": "로그 데이터는 엔진 내부로 재유입되지 않는다 (No Feedback).",
    "ER-LOG-001.c": "로그 기록 실패는 엔진 판단에 영향을 주지 않는다 (Fail-Safe Write).",
    "ER-LOG-001.d": "외부 반출(SCP/S3/rsync 등)은 엔진 외부 책임이다.",
}

# ============================================================
# [ER-STATE] STATE_MANAGER / PERSISTENCE  ★ 추가 (기존 내용 유지)
# ============================================================
ER_ID.update({

    # --- STATE FACTS / SCHEMA ---
    "ER-STATE-010": "STATE_MANAGER는 해석 없는 사실(Facts)만 저장한다 (의미·판단 금지).",
    "ER-STATE-011": "상태 스키마는 엔진 재시작 후에도 복구 가능해야 한다.",

    # --- ATOMIC PERSISTENCE ---
    "ER-STATE-012": "상태 저장은 반드시 atomic write(os.replace)로 수행한다.",
    "ER-STATE-013": "상태 로드 실패/손상 시 엔진은 안전 기본 상태로 복구한다.",

    # --- SCHEMA COMPATIBILITY ---
    "ER-STATE-014": "상태 스키마 변경 시 누락 키는 기본값으로 보정한다.",
    "ER-STATE-015": "알 수 없는 상태 키는 무시한다 (forward/backward compatibility).",

    # --- STATE TRANSITIONS ---
    "ER-STATE-016": "상태 전이 함수는 사실 업데이트만 수행한다.",
    "ER-STATE-017": "전이 함수는 주문·판단·전략 로직을 포함하지 않는다.",

    # --- COUNTERS / TICKS ---
    "ER-STATE-018": "카운터 증가는 bar/tick 이벤트에 의해 단조 증가한다.",

})

# ============================================================
# [ER-CFG-000] CFG ROOT OBJECT
# ============================================================
CFG = {

    # =====================================================
    # [CFG][PRIORITY 0]
    # CFG-001 CAPITAL / POSITION BASE
    # =====================================================
    "0_TRADE_SYMBOL": "TIAUSDT.P",
    "0_CAPITAL_BASE_USDT": 60,
    "0_CAPITAL_USE_FIXED": True,
    "0_CAPITAL_MAX_LOSS_PCT": 100.0,


    # =====================================================
    # [CFG][PRIORITY 1]
    # CFG-002 GLOBAL / SAFETY
    # =====================================================
    "1_ENGINE_ENABLE": True,
    "2_ENTRY_CANDIDATE_ENABLE": True,
    "3_ENTRY_EXEC_ENABLE": True,


    # =====================================================
    # [CFG][PRIORITY 2]
    # CFG-003 ENTRY CANDIDATE PARAMETERS
    # =====================================================
    "4_EMA_PERIOD": 9,
    "5_CAND_BODY_BELOW_EMA": True,
    "6_CAND_USE_CLOSE_ONLY": False,


    # =====================================================
    # [CFG][PRIORITY 3]
    # CFG-004 COOLDOWN PARAMETERS
    # =====================================================
    "7_ENTRY_COOLDOWN_BARS": 2,
    "8_ENTRY_COOLDOWN_AFTER_EXIT": 1,


    # =====================================================
    # [CFG][PRIORITY 4]
    # CFG-005 RE-ENTRY CONTROL PARAMETERS
    # =====================================================
    "9_REENTRY_SAME_REASON_BLOCK": True,
    "10_ENTRY_LOOKBACK_BARS": 5,
    "11_REENTRY_PRICE_TOL_PCT": 0.15,


    # =====================================================
    # [CFG][PRIORITY 5]
    # CFG-006 STATE-BASED MODULATION
    # =====================================================
    "12_STATE_COOLDOWN_ENABLE": True,
    "13_COOLDOWN_RANGE_BARS": 4,
    "14_COOLDOWN_TREND_BARS": 1,


    # =====================================================
    # [CFG][PRIORITY 6]
    # CFG-007 CANDIDATE POOL PARAMETERS
    # =====================================================
    "15_CAND_POOL_TTL_BARS": 6,
    "16_CAND_POOL_MAX_SIZE": 3,
    "17_CAND_MIN_GAP_BARS": 1,


    # =====================================================
    # [CFG][PRIORITY 7]
    # CFG-008 LIMIT / FAIL-SAFE
    # =====================================================
    "18_ENTRY_MAX_PER_CYCLE": 1,
    "19_MAX_ENTRIES_PER_DAY": 20,
    "20_DATA_STALE_BLOCK": True,


    # =====================================================
    # [CFG][PRIORITY 8]
    # CFG-009 VOLATILITY CONTROL
    # =====================================================
    "21_VOLATILITY_BLOCK_ENABLE": False,
    "22_VOLATILITY_MAX_PCT": 2.5,


    # =====================================================
    # [CFG][PRIORITY 9]
    # CFG-010 LOG / DEBUG
    # =====================================================
    "23_LOG_CANDIDATES": True,
    "24_LOG_EXECUTIONS": True,
    "25_DEBUG_LABEL_ENABLE": False,
}


# ============================================================
# [ENGINE_RULE] CFG ACCESS FUNCTIONS
# ============================================================

# ============================================================
# [ER-CFG-011] GET TRADE SYMBOL CONTRACT
# ============================================================
def get_trade_symbol(cfg: dict) -> str:
    """
    [ENGINE_RULE][ER-CFG-011]
    INPUT  : cfg
    OUTPUT : trade symbol (str)
    EXCEPT : empty / missing symbol
    """
    symbol = cfg.get("0_TRADE_SYMBOL", "").strip()
    if not symbol:
        raise RuntimeError("CFG ERROR: 0_TRADE_SYMBOL is empty")
    return symbol


# ============================================================
# [ER-CFG-012] GET CAPITAL BASE CONTRACT
# ============================================================
def get_capital_base(cfg: dict) -> float:
    """
    [ENGINE_RULE][ER-CFG-012]
    INPUT  : cfg
    OUTPUT : capital base (float)
    """
    return float(cfg["0_CAPITAL_BASE_USDT"])


import os, json, time
from typing import Any, Dict, Tuple, Optional


# ============================================================
# [ENGINE_RULE]
# [ER-CFGM-001] SOURCE & DEFAULTS
# ============================================================
CFG_DEFAULTS: Dict[str, Any] = {
    # --- Capital ---
    "0_CAPITAL_BASE_USDT": 200.0,              # ER-CFGM-001-A
    "0_CAPITAL_USE_FIXED": True,               # ER-CFGM-001-B
    "0_CAPITAL_MAX_LOSS_PCT": 100.0,           # ER-CFGM-001-C

    # --- Global ---
    "1_ENGINE_ENABLE": True,                   # ER-CFGM-001-D
    "2_ENTRY_CANDIDATE_ENABLE": True,          # ER-CFGM-001-E
    "3_ENTRY_EXEC_ENABLE": True,               # ER-CFGM-001-F

    # --- Entry / EMA ---
    "4_EMA_PERIOD": 9,                         # ER-CFGM-001-G
    "5_CAND_BODY_BELOW_EMA": True,             # ER-CFGM-001-H
    "6_CAND_USE_CLOSE_ONLY": False,            # ER-CFGM-001-I

    # --- Cooldown ---
    "7_ENTRY_COOLDOWN_BARS": 2,                # ER-CFGM-001-J
    "8_ENTRY_COOLDOWN_AFTER_EXIT": 1,          # ER-CFGM-001-K

    # --- Re-entry ---
    "9_REENTRY_SAME_REASON_BLOCK": True,       # ER-CFGM-001-L
    "10_ENTRY_LOOKBACK_BARS": 5,               # ER-CFGM-001-M
    "11_REENTRY_PRICE_TOL_PCT": 0.15,          # ER-CFGM-001-N

    # --- State ---
    "12_STATE_COOLDOWN_ENABLE": True,          # ER-CFGM-001-O
    "13_COOLDOWN_RANGE_BARS": 4,               # ER-CFGM-001-P
    "14_COOLDOWN_TREND_BARS": 1,               # ER-CFGM-001-Q

    # --- Pool ---
    "15_CAND_POOL_TTL_BARS": 6,                # ER-CFGM-001-R
    "16_CAND_POOL_MAX_SIZE": 3,                # ER-CFGM-001-S
    "17_CAND_MIN_GAP_BARS": 1,                 # ER-CFGM-001-T

    # --- Limits ---
    "18_ENTRY_MAX_PER_CYCLE": 1,               # ER-CFGM-001-U
    "19_MAX_ENTRIES_PER_DAY": 6,               # ER-CFGM-001-V
    "20_DATA_STALE_BLOCK": True,               # ER-CFGM-001-W

    # --- Volatility ---
    "21_VOLATILITY_BLOCK_ENABLE": False,       # ER-CFGM-001-X
    "22_VOLATILITY_MAX_PCT": 2.5,              # ER-CFGM-001-Y

    # --- Logging ---
    "23_LOG_CANDIDATES": True,                 # ER-CFGM-001-Z
    "24_LOG_EXECUTIONS": True,                 # ER-CFGM-001-AA
    "25_DEBUG_LABEL_ENABLE": False,            # ER-CFGM-001-AB

    # --- State file ---
    "STATE_FILE": "v4_state.json",             # ER-CFGM-001-AC
}


# ============================================================
# [ENGINE_RULE]
# [ER-CFGM-002] VALIDATION SPECS
# ============================================================
# - 최소한의 타입/범위만 검증 (의미 해석 금지)
SPEC = {
    # floats
    "0_CAPITAL_BASE_USDT": ("float", 0.0, 1e12),        # ER-CFGM-002-A
    "0_CAPITAL_MAX_LOSS_PCT": ("float", 0.0, 100.0),   # ER-CFGM-002-B
    "22_VOLATILITY_MAX_PCT": ("float", 0.0, 1000.0),   # ER-CFGM-002-C
    "11_REENTRY_PRICE_TOL_PCT": ("float", 0.0, 100.0), # ER-CFGM-002-D

    # ints
    "4_EMA_PERIOD": ("int", 1, 500),                   # ER-CFGM-002-E
    "7_ENTRY_COOLDOWN_BARS": ("int", 0, 10_000),       # ER-CFGM-002-F
    "8_ENTRY_COOLDOWN_AFTER_EXIT": ("int", 0, 10_000), # ER-CFGM-002-G
    "10_ENTRY_LOOKBACK_BARS": ("int", 1, 10_000),      # ER-CFGM-002-H
    "13_COOLDOWN_RANGE_BARS": ("int", 0, 10_000),      # ER-CFGM-002-I
    "14_COOLDOWN_TREND_BARS": ("int", 0, 10_000),      # ER-CFGM-002-J
    "15_CAND_POOL_TTL_BARS": ("int", 0, 10_000),       # ER-CFGM-002-K
    "16_CAND_POOL_MAX_SIZE": ("int", 0, 10_000),       # ER-CFGM-002-L
    "17_CAND_MIN_GAP_BARS": ("int", 0, 10_000),        # ER-CFGM-002-M
    "18_ENTRY_MAX_PER_CYCLE": ("int", 0, 10_000),      # ER-CFGM-002-N
    "19_MAX_ENTRIES_PER_DAY": ("int", 0, 10_000),      # ER-CFGM-002-O

    # bools
    "0_CAPITAL_USE_FIXED": ("bool",),                  # ER-CFGM-002-P
    "1_ENGINE_ENABLE": ("bool",),                      # ER-CFGM-002-Q
    "2_ENTRY_CANDIDATE_ENABLE": ("bool",),             # ER-CFGM-002-R
    "3_ENTRY_EXEC_ENABLE": ("bool",),                  # ER-CFGM-002-S
    "5_CAND_BODY_BELOW_EMA": ("bool",),                # ER-CFGM-002-T
    "6_CAND_USE_CLOSE_ONLY": ("bool",),                # ER-CFGM-002-U
    "9_REENTRY_SAME_REASON_BLOCK": ("bool",),          # ER-CFGM-002-V
    "12_STATE_COOLDOWN_ENABLE": ("bool",),             # ER-CFGM-002-W
    "20_DATA_STALE_BLOCK": ("bool",),                  # ER-CFGM-002-X
    "21_VOLATILITY_BLOCK_ENABLE": ("bool",),           # ER-CFGM-002-Y
    "23_LOG_CANDIDATES": ("bool",),                    # ER-CFGM-002-Z
    "24_LOG_EXECUTIONS": ("bool",),                    # ER-CFGM-002-AA
    "25_DEBUG_LABEL_ENABLE": ("bool",),                # ER-CFGM-002-AB

    # str
    "STATE_FILE": ("str",),                            # ER-CFGM-002-AC
}


# ============================================================
# [ENGINE_RULE]
# [ER-CFGM-003] LOADING
# ============================================================
def load_cfg_file(path: str) -> Dict[str, Any]:
    """
    [ENGINE_RULE][ER-CFGM-003]
    - JSON만 지원
    - 파일 없으면 빈 dict
    """
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f) or {}


def merge_cfg(defaults: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    [ENGINE_RULE][ER-CFGM-004]
    - defaults 위에 override 덮어쓰기
    """
    out = dict(defaults)
    for k, v in (override or {}).items():
        out[k] = v
    return out


# ============================================================
# [ENGINE_RULE]
# [ER-CFGM-005] VALIDATION
# ============================================================
def _coerce_type(val: Any, t: str) -> Any:
    if t == "int":
        return int(val)
    if t == "float":
        return float(val)
    if t == "bool":
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            s = val.strip().lower()
            if s in ("true", "1", "yes", "y", "on"):
                return True
            if s in ("false", "0", "no", "n", "off"):
                return False
        return bool(val)
    if t == "str":
        return str(val)
    return val


def validate_cfg(cfg: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
    """
    [ENGINE_RULE][ER-CFGM-006]
    - ok, validated_cfg, error_message
    - 의미 해석 금지: 타입/범위만 체크
    """
    out = dict(cfg)
    for k, spec in SPEC.items():
        if k not in out:
            continue
        t = spec[0]

        try:
            out[k] = _coerce_type(out[k], t)
        except Exception:
            return False, cfg, f"CFG_TYPE_ERROR:{k}"

        if t in ("int", "float") and len(spec) == 3:
            lo, hi = spec[1], spec[2]
            if not (lo <= out[k] <= hi):
                return False, cfg, f"CFG_RANGE_ERROR:{k}"

    return True, out, ""


# ============================================================
# [ENGINE_RULE]
# [ER-CFGM-007] SNAPSHOT / HOT RELOAD
# ============================================================
class CfgManager:
    """
    [ENGINE_RULE][ER-CFGM-007]
    - cfg 파일을 로드하고 검증한 스냅샷 제공
    """
    def __init__(self, cfg_path: str = ""):
        self.cfg_path = cfg_path
        self.last_mtime: float = 0.0
        self.cfg: Dict[str, Any] = dict(CFG_DEFAULTS)
        self.last_error: str = ""

    def load_once(self) -> Dict[str, Any]:
        """
        [ENGINE_RULE][ER-CFGM-008]
        """
        raw = load_cfg_file(self.cfg_path)
        merged = merge_cfg(CFG_DEFAULTS, raw)
        ok, validated, err = validate_cfg(merged)
        if ok:
            self.cfg = validated
            self.last_error = ""
        else:
            self.last_error = err
        return self.cfg

    def hot_reload_if_changed(self) -> Dict[str, Any]:
        """
        [ENGINE_RULE][ER-CFGM-009]
        - 파일 변경 시에만 재로드
        """
        if not self.cfg_path or not os.path.exists(self.cfg_path):
            return self.cfg

        mtime = os.path.getmtime(self.cfg_path)
        if mtime > self.last_mtime:
            self.last_mtime = mtime
            return self.load_once()

        return self.cfg



# ============================================================
# (17) SYMBOL_RESOLVER_MODULE — V4
# ENGINE_RULE / HUMAN_NOTE SPLIT TEMPLATE
# ============================================================

from dataclasses import dataclass

# ============================================================
# [ENGINE_RULE]
# [ER-SYM-001] SYMBOL INFO (STANDARDIZED)
# ============================================================
@dataclass(frozen=True)
class SymbolInfo:
    raw: str            # ER-SYM-001-A : CFG 원본 (예: "TIAUSDT.P")
    base: str           # ER-SYM-001-B : 거래소 API 심볼 (예: "TIAUSDT")
    market: str         # ER-SYM-001-C : "FUTURES" | "SPOT"
    display: str        # ER-SYM-001-D : 로그/표시용

# ============================================================
# [ENGINE_RULE]
# [ER-SYM-002] RESOLVE FUNCTION (SINGLE SOURCE OF TRUTH)
# ============================================================
def resolve_symbol(cfg: dict) -> SymbolInfo:
    """
    [ENGINE_RULE][ER-SYM-002]
    INPUT  : cfg
    OUTPUT : SymbolInfo
    EXCEPT : invalid / empty symbol
    """
    raw = str(cfg.get("0_TRADE_SYMBOL", "")).strip()
    if not raw:
        raise RuntimeError("CFG ERROR: 0_TRADE_SYMBOL is empty")  # ER-SYM-002-A

    # ========================================================
    # [ER-SYM-003] FUTURES DISPLAY TAG RULE ('.P')
    # ========================================================
    if raw.endswith(".P"):
        base = raw[:-2].strip()
        if not base:
            raise RuntimeError("CFG ERROR: 0_TRADE_SYMBOL invalid ('.P' only)")  # ER-SYM-003-A
        return SymbolInfo(
            raw=raw,                     # ER-SYM-003-B
            base=base,                   # ER-SYM-003-C
            market="FUTURES",            # ER-SYM-003-D
            display=raw,                 # ER-SYM-003-E
        )

    # ========================================================
    # [ER-SYM-004] DEFAULT FUTURES RULE
    # ========================================================
    return SymbolInfo(
        raw=raw,                         # ER-SYM-004-A
        base=raw,                        # ER-SYM-004-B
        market="FUTURES",                # ER-SYM-004-C
        display=raw,                     # ER-SYM-004-D
    )

# ============================================================
# [ENGINE_RULE]
# [ER-ENTRY-002] CANDIDATE REGISTRATION
# ============================================================
def register_entry_candidate(candle, ema_value, state, cfg):
    """
    [ENGINE_RULE][ER-ENTRY-002]
    - 조건 충족 시 후보를 '등록'만 한다
    """
    if not cfg["2_ENTRY_CANDIDATE_ENABLE"]:
        return                                  # ER-ENTRY-002-A

    body_low = min(candle.open, candle.close)
    if cfg["5_CAND_BODY_BELOW_EMA"] and body_low < ema_value:
        state.add_candidate(
            reason="EMA_BODY_BELOW",            # ER-ENTRY-002-B
            price=candle.close,                 # ER-ENTRY-002-C
            ts=candle.ts                        # ER-ENTRY-002-D
        )

# ============================================================
# [ENGINE_RULE]
# [ER-ENTRY-003] EXECUTION GATE
# ============================================================
def execution_gate(state, cfg):
    """
    [ENGINE_RULE][ER-ENTRY-003]
    - 실행 가능 여부만 반환
    """
    if not cfg["1_ENGINE_ENABLE"] or not cfg["3_ENTRY_EXEC_ENABLE"]:
        return False                            # ER-ENTRY-003-A

    # ========================================================
    # [ER-ENTRY-004] BASIC COOLDOWN
    # ========================================================
    if state.bars_since_last_entry < cfg["7_ENTRY_COOLDOWN_BARS"]:
        return False                            # ER-ENTRY-004-A

    # ========================================================
    # [ER-ENTRY-005] POST-EXIT COOLDOWN
    # ========================================================
    if state.bars_since_last_exit < cfg["8_ENTRY_COOLDOWN_AFTER_EXIT"]:
        return False                            # ER-ENTRY-005-A

    # ========================================================
    # [ER-ENTRY-006] SAME REASON RE-ENTRY BLOCK
    # ========================================================
    if cfg["9_REENTRY_SAME_REASON_BLOCK"]:
        if state.is_same_reason_within(
            lookback=cfg["10_ENTRY_LOOKBACK_BARS"],      # ER-ENTRY-006-A
            price_tol_pct=cfg["11_REENTRY_PRICE_TOL_PCT"]# ER-ENTRY-006-B
        ):
            return False                                  # ER-ENTRY-006-C

    # ========================================================
    # [ER-ENTRY-007] STATE-BASED COOLDOWN
    # ========================================================
    if cfg["12_STATE_COOLDOWN_ENABLE"]:
        if state.market_state == "RANGE":
            if state.bars_since_last_entry < cfg["13_COOLDOWN_RANGE_BARS"]:
                return False                              # ER-ENTRY-007-A
        if state.market_state == "TREND":
            if state.bars_since_last_entry < cfg["14_COOLDOWN_TREND_BARS"]:
                return False                              # ER-ENTRY-007-B

# =====================================================
# [ER-BTC-001] BTC REGIME FILTER (V6)
# - 시장 조건 필터 (LIMIT 아님)
# - STATE 쿨다운 이후 / LIMIT 이전 평가
# =====================================================

if cfg.get("30_BTC_REGIME_ENABLE", False):
    mode = str(cfg.get("31_BTC_REGIME_MODE", "PULSE")).upper()

    if mode != "OFF":
        ok = btc_regime_ok(state, cfg)

        if mode == "STRICT":
            if not ok:
                return False   # ER-BTC-001-A
        else:
            # PULSE (완화형)
            if not ok:
                return False   # ER-BTC-001-B


    # ========================================================
    # [ER-ENTRY-008] LIMIT / FAIL-SAFE
    # ========================================================
    if state.entries_today >= cfg["19_MAX_ENTRIES_PER_DAY"]:
        return False                                      # ER-ENTRY-008-A
    if state.entries_in_cycle >= cfg["18_ENTRY_MAX_PER_CYCLE"]:
  
        return False                                      # ER-ENTRY-008-B

    return True                                           # ER-ENTRY-003-Z

# ============================================================
# [ENGINE_RULE]
# [ER-ENTRY-009] ENTRY EXECUTION
# ============================================================
def execute_entry_if_allowed(state, cfg):
    """
    [ENGINE_RULE][ER-ENTRY-009]
    - 후보가 있고 게이트 통과 시 실행
    """
    if not state.has_candidate():
        return False                                      # ER-ENTRY-009-A

    if execution_gate(state, cfg):
        state.execute_entry()                             # ER-ENTRY-009-B
        state.clear_candidates()                          # ER-ENTRY-009-C
        return True                                       # ER-ENTRY-009-D

    return False                                          # ER-ENTRY-009-E

# ============================================================
# [ENGINE_RULE]
# [ER-ENTRY-010] ENTRY PIPELINE (SINGLE BAR)
# ============================================================
def entry_engine_step(candle, ema_value, state, cfg):
    """
    [ENGINE_RULE][ER-ENTRY-010]
    - 한 봉당 호출되는 엔트리 파이프라인
    """
    register_entry_candidate(candle, ema_value, state, cfg)  # ER-ENTRY-010-A
    execute_entry_if_allowed(state, cfg)                     # ER-ENTRY-010-B


# ============================================================
# [ENGINE_RULE]
# [ER-EXIT-002] EXIT CFG DEFAULT KEYS (DECLARATION)
# ============================================================
EXIT_CFG_KEYS = {
    "EXIT_ENABLE": True,                    # ER-EXIT-002-A

    "TP1_ENABLE": True,                     # ER-EXIT-002-B
    "TP1_RR_PCT": 0.30,                     # ER-EXIT-002-C
    "TP1_QTY_PCT": 50.0,                    # ER-EXIT-002-D

    "SL_ENABLE": True,                      # ER-EXIT-002-E
    "SL_PCT": 0.50,                         # ER-EXIT-002-F

    "TRAIL_ENABLE": True,                   # ER-EXIT-002-G
    "TRAIL_AFTER_TP1": True,                # ER-EXIT-002-H
    "TRAIL_GAP_PCT": 0.25,                  # ER-EXIT-002-I

    "EXIT_3M_LOOKBACK": 3,                  # ER-EXIT-002-J
    "FORCE_EXIT_ON_ENGINE_ERROR": True,     # ER-EXIT-002-K
}

# ============================================================
# [ENGINE_RULE]
# [ER-EXIT-003] UTILS
# ============================================================
def pct_move(from_price, to_price):
    """
    [ENGINE_RULE][ER-EXIT-003]
    """
    if from_price == 0:
        return 0.0                           # ER-EXIT-003-A
    return (to_price - from_price) / from_price * 100.0  # ER-EXIT-003-B


def clamp_qty(qty, min_qty=0.0):
    """
    [ENGINE_RULE][ER-EXIT-004]
    """
    return qty if qty > min_qty else 0.0     # ER-EXIT-004-A

# ============================================================
# [ENGINE_RULE]
# [ER-EXIT-005] EXIT DECISION — TP1
# ============================================================
def should_take_tp1(state, last_price, cfg):
    """
    [ENGINE_RULE][ER-EXIT-005]
    """
    if not cfg.get("EXIT_ENABLE", True):
        return False                         # ER-EXIT-005-A
    if not cfg.get("TP1_ENABLE", True):
        return False                         # ER-EXIT-005-B
    if state.tp1_done:
        return False                         # ER-EXIT-005-C

    move_pct = pct_move(state.entry_price, last_price)
    profit_pct = -move_pct                  # ER-EXIT-005-D

    return profit_pct >= float(cfg.get("TP1_RR_PCT", 0.30))  # ER-EXIT-005-E


def tp1_qty(state, cfg):
    """
    [ENGINE_RULE][ER-EXIT-006]
    """
    pct = float(cfg.get("TP1_QTY_PCT", 50.0)) / 100.0       # ER-EXIT-006-A
    return clamp_qty(state.qty * pct)                        # ER-EXIT-006-B

# ============================================================
# [ENGINE_RULE]
# [ER-EXIT-007] EXIT DECISION — SL
# ============================================================
def should_stop_loss(state, last_price, cfg):
    """
    [ENGINE_RULE][ER-EXIT-007]
    """
    if not cfg.get("EXIT_ENABLE", True):
        return False                         # ER-EXIT-007-A
    if not cfg.get("SL_ENABLE", True):
        return False                         # ER-EXIT-007-B

    move_pct = pct_move(state.entry_price, last_price)
    loss_pct = move_pct                     # ER-EXIT-007-C

    return loss_pct >= float(cfg.get("SL_PCT", 0.50))       # ER-EXIT-007-D

# ============================================================
# [ENGINE_RULE]
# [ER-EXIT-008] TRAILING UPDATE
# ============================================================
def update_trailing(state, last_price, cfg):
    """
    [ENGINE_RULE][ER-EXIT-008]
    """
    if not cfg.get("EXIT_ENABLE", True):
        return                               # ER-EXIT-008-A
    if not cfg.get("TRAIL_ENABLE", True):
        return                               # ER-EXIT-008-B
    if cfg.get("TRAIL_AFTER_TP1", True) and (not state.tp1_done):
        return                               # ER-EXIT-008-C

    gap_pct = float(cfg.get("TRAIL_GAP_PCT", 0.25))         # ER-EXIT-008-D

    if state.trailing_low is None or last_price < state.trailing_low:
        state.trailing_low = last_price                    # ER-EXIT-008-E
        state.trailing_stop = last_price * (1.0 + gap_pct / 100.0)  # ER-EXIT-008-F
        state.trailing_active = True                       # ER-EXIT-008-G


def should_trailing_exit(state, last_price, cfg):
    """
    [ENGINE_RULE][ER-EXIT-009]
    """
    if not cfg.get("EXIT_ENABLE", True):
        return False                         # ER-EXIT-009-A
    if not cfg.get("TRAIL_ENABLE", True):
        return False                         # ER-EXIT-009-B
    if not state.trailing_active:
        return False                         # ER-EXIT-009-C
    if state.trailing_stop is None:
        return False                         # ER-EXIT-009-D

    return last_price >= state.trailing_stop # ER-EXIT-009-E

# ============================================================
# [ENGINE_RULE]
# [ER-EXIT-010] EXIT PIPELINE (SINGLE TICK/BAR)
# ============================================================
def exit_engine_step(last_price, state, cfg, execution, symbol):
    """
    [ENGINE_RULE][ER-EXIT-010]
    """
    if not state.has_position:
        return                               # ER-EXIT-010-A
    if not cfg.get("EXIT_ENABLE", True):
        return                               # ER-EXIT-010-B

    # SL 우선
    if should_stop_loss(state, last_price, cfg):
        res = execution.place_reduce_only(
            exchange=state.exchange,
            symbol=symbol,
            side="BUY",
            qty=state.qty,
            cfg=state.exec_cfg,
            state=state,
            client_id="EXIT_SL"              # ER-EXIT-010-C
        )
        if res.ok:
            state.on_exit(reason="SL", price=last_price)  # ER-EXIT-010-D
        return

    # TP1
    if should_take_tp1(state, last_price, cfg):
        q = tp1_qty(state, cfg)
        if q > 0:
            res = execution.place_reduce_only(
                exchange=state.exchange,
                symbol=symbol,
                side="BUY",
                qty=q,
                cfg=state.exec_cfg,
                state=state,
                client_id="EXIT_TP1"         # ER-EXIT-010-E
            )
            if res.ok:
                state.on_tp1(price=last_price, qty=q)     # ER-EXIT-010-F

    # trailing update
    update_trailing(state, last_price, cfg)

    # trailing exit
    if should_trailing_exit(state, last_price, cfg):
        res = execution.place_reduce_only(
            exchange=state.exchange,
            symbol=symbol,
            side="BUY",
            qty=state.qty,
            cfg=state.exec_cfg,
            state=state,
            client_id="EXIT_TRAIL"           # ER-EXIT-010-G
        )
        if res.ok:
            state.on_exit(reason="TRAIL", price=last_price)  # ER-EXIT-010-H
        return



# ============================================================
# DATA_FEED_MODULE — V4 (SYMBOL-AGNOSTIC MARKET DATA ADAPTER)
# ENGINE_RULE / HUMAN_NOTE SPLIT TEMPLATE
# ============================================================


import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# ============================================================
# [ENGINE_RULE]
# [ER-FEED-002] CANONICAL CANDLE STRUCT
# ============================================================
@dataclass
class Candle:
    ts: int                # ER-FEED-002-A
    open: float            # ER-FEED-002-B
    high: float            # ER-FEED-002-C
    low: float             # ER-FEED-002-D
    close: float           # ER-FEED-002-E
    vol: float             # ER-FEED-002-F
    is_closed: bool        # ER-FEED-002-G

# ============================================================
# [ENGINE_RULE]
# [ER-FEED-003] DATA FEED CFG DEFAULTS
# ============================================================
FEED_CFG_DEFAULTS = {
    "FEED_ENABLE": True,           # ER-FEED-003-A
    "KEEP": 200,                   # ER-FEED-003-B
    "STALE_MS": 120_000,           # ER-FEED-003-C
    "SNAPSHOT_LIMIT": 200,         # ER-FEED-003-D
    "POLL_SEC": 2.0,               # ER-FEED-003-E
    "USE_WS": False,               # ER-FEED-003-F
}

# ============================================================
# [ENGINE_RULE]
# [ER-FEED-004] EXCHANGE ADAPTER INTERFACE
# ============================================================
class ExchangeDataAdapter:
    """
    [ENGINE_RULE][ER-FEED-004]
    - 거래소 구현체 인터페이스
    - 심볼/타임프레임만 받는다
    """

    def fetch_klines_snapshot(self, symbol: str, tf: str, limit: int) -> List[dict]:
        """
        [ENGINE_RULE][ER-FEED-004-A]
        """
        raise NotImplementedError

    def poll_latest_kline(self, symbol: str, tf: str) -> Optional[dict]:
        """
        [ENGINE_RULE][ER-FEED-004-B]
        """
        raise NotImplementedError

    def ws_subscribe_klines(self, symbol: str, tf: str, on_message):
        """
        [ENGINE_RULE][ER-FEED-004-C]
        """
        raise NotImplementedError

# ============================================================
# [ENGINE_RULE]
# [ER-FEED-005] NORMALIZATION
# ============================================================
def normalize_kline(raw: dict) -> Candle:
    """
    [ENGINE_RULE][ER-FEED-005]
    - 거래소 원본 → Candle
    """
    return Candle(
        ts=int(raw["ts"]),                  # ER-FEED-005-A
        open=float(raw["open"]),             # ER-FEED-005-B
        high=float(raw["high"]),             # ER-FEED-005-C
        low=float(raw["low"]),               # ER-FEED-005-D
        close=float(raw["close"]),           # ER-FEED-005-E
        vol=float(raw.get("vol", 0.0)),      # ER-FEED-005-F
        is_closed=bool(raw.get("is_closed", True)),  # ER-FEED-005-G
    )

# ============================================================
# [ENGINE_RULE]
# [ER-FEED-006] CANDLE BUFFER
# ============================================================
class CandleBuffer:
    """
    [ENGINE_RULE][ER-FEED-006]
    - 완료봉/진행중봉 단일 진실
    """
    def __init__(self, keep: int):
        self.keep = keep                         # ER-FEED-006-A
        self.candles: List[Candle] = []          # ER-FEED-006-B
        self.last_update_ms: int = 0             # ER-FEED-006-C

    def set_snapshot(self, candles: List[Candle]):
        self.candles = candles[-self.keep:]      # ER-FEED-006-D
        self.last_update_ms = int(time.time() * 1000)  # ER-FEED-006-E

    def upsert(self, c: Candle):
        """
        [ENGINE_RULE][ER-FEED-006-F]
        - ts 기준 동일 캔들 갱신
        """
        if not self.candles:
            self.candles = [c]                   # ER-FEED-006-G
            self.last_update_ms = int(time.time() * 1000)
            return

        if self.candles[-1].ts == c.ts:
            self.candles[-1] = c                 # ER-FEED-006-H
        elif self.candles[-1].ts < c.ts:
            self.candles.append(c)               # ER-FEED-006-I
        else:
            return                               # ER-FEED-006-J

        if len(self.candles) > self.keep:
            self.candles = self.candles[-self.keep:]  # ER-FEED-006-K

        self.last_update_ms = int(time.time() * 1000)  # ER-FEED-006-L

    def get_all(self) -> List[Candle]:
        return self.candles                      # ER-FEED-006-M

    def get_closed(self) -> List[Candle]:
        return [x for x in self.candles if x.is_closed]  # ER-FEED-006-N

    def is_stale(self, stale_ms: int) -> bool:
        now = int(time.time() * 1000)
        return (now - self.last_update_ms) > stale_ms    # ER-FEED-006-O

# ============================================================
# [ENGINE_RULE]
# [ER-FEED-007] DATA FEED MANAGER
# ============================================================
class DataFeed:
    """
    [ENGINE_RULE][ER-FEED-007]
    - (symbol, tf)별 버퍼 관리
    """
    def __init__(self, adapter: ExchangeDataAdapter, cfg: dict):
        self.adapter = adapter                                  # ER-FEED-007-A
        self.cfg = {**FEED_CFG_DEFAULTS, **(cfg or {})}         # ER-FEED-007-B
        self.buffers: Dict[Tuple[str, str], CandleBuffer] = {} # ER-FEED-007-C

    def _buf(self, symbol: str, tf: str) -> CandleBuffer:
        key = (symbol, tf)
        if key not in self.buffers:
            self.buffers[key] = CandleBuffer(keep=int(self.cfg["KEEP"]))  # ER-FEED-007-D
        return self.buffers[key]

    # --------------------------------------------------------
    # [ENGINE_RULE]
    # [ER-FEED-008] SNAPSHOT INIT
    # --------------------------------------------------------
    def init_snapshot(self, symbol_info, tf: str):
        if not self.cfg["FEED_ENABLE"]:
            return                                            # ER-FEED-008-A
        symbol = symbol_info.base                              # ER-FEED-008-B

        limit = int(self.cfg["SNAPSHOT_LIMIT"])               # ER-FEED-008-C
        raw_list = self.adapter.fetch_klines_snapshot(symbol, tf, limit)
        candles = [normalize_kline(r) for r in raw_list]
        self._buf(symbol, tf).set_snapshot(candles)

        if self.cfg["USE_WS"]:
            self.adapter.ws_subscribe_klines(
                symbol, tf, lambda raw: self.on_ws_kline(symbol, tf, raw)
            )                                                  # ER-FEED-008-D

    # --------------------------------------------------------
    # [ENGINE_RULE]
    # [ER-FEED-009] POLL STEP
    # --------------------------------------------------------
    def poll_step(self, symbol_info, tf: str):
        if not self.cfg["FEED_ENABLE"]:
            return                                            # ER-FEED-009-A
        if self.cfg["USE_WS"]:
            return                                            # ER-FEED-009-B
        symbol = symbol_info.base                              # ER-FEED-009-C

        raw = self.adapter.poll_latest_kline(symbol, tf)
        if raw is None:
            return                                            # ER-FEED-009-D
        c = normalize_kline(raw)
        self._buf(symbol, tf).upsert(c)

    def get_candles(self, symbol_info, tf: str) -> List[Candle]:
        symbol = symbol_info.base                              # ER-FEED-009-E
        return self._buf(symbol, tf).get_all()

    def is_stale(self, symbol_info, tf: str) -> bool:
        symbol = symbol_info.base                              # ER-FEED-009-F
        stale_ms = int(self.cfg["STALE_MS"])                   # ER-FEED-009-G
        return self._buf(symbol, tf).is_stale(stale_ms)

    # --------------------------------------------------------
    # [ENGINE_RULE]
    # [ER-FEED-010] WS HANDLER
    # --------------------------------------------------------
    def on_ws_kline(self, symbol: str, tf: str, raw: dict):
        c = normalize_kline(raw)                               # ER-FEED-010-A
        self._buf(symbol, tf).upsert(c)


# ============================================================
# INDICATOR_MODULE — V4 (NUMERIC PRODUCER ONLY)
# ENGINE_RULE / HUMAN_NOTE SPLIT TEMPLATE
# ============================================================

from typing import List, Dict
from dataclasses import dataclass

# ============================================================
# [ENGINE_RULE]
# [ER-IND-001] CANONICAL INPUT
# ============================================================
@dataclass
class Candle:
    ts: int           # ER-IND-001-A
    open: float       # ER-IND-001-B
    high: float       # ER-IND-001-C
    low: float        # ER-IND-001-D
    close: float      # ER-IND-001-E
    vol: float        # ER-IND-001-F
    is_closed: bool   # ER-IND-001-G

# ============================================================
# [ENGINE_RULE]
# [ER-IND-002] INDICATOR CFG DEFAULTS (READ-ONLY)
# ============================================================
IND_CFG_DEFAULTS = {
    "IND_EMA_ENABLE": True,          # ER-IND-002-A
    "IND_EMA_PERIOD": 9,             # ER-IND-002-B

    "IND_ATR_ENABLE": False,         # ER-IND-002-C
    "IND_ATR_PERIOD": 14,            # ER-IND-002-D

    "IND_VOL_ENABLE": False,         # ER-IND-002-E
    "IND_VOL_LOOKBACK": 10,          # ER-IND-002-F

    "IND_SLOPE_ENABLE": False,       # ER-IND-002-G
    "IND_SLOPE_LOOKBACK": 5,         # ER-IND-002-H
}

# ============================================================
# [ENGINE_RULE]
# [ER-IND-003] UTILS — EMA
# ============================================================
def _ema(values: List[float], period: int) -> List[float]:
    """
    [ENGINE_RULE][ER-IND-003]
    """
    if period <= 0 or not values:
        return []                                  # ER-IND-003-A
    k = 2.0 / (period + 1.0)                      # ER-IND-003-B
    ema = []
    for i, v in enumerate(values):
        if i == 0:
            ema.append(v)                         # ER-IND-003-C
        else:
            ema.append(v * k + ema[-1] * (1.0 - k))  # ER-IND-003-D
    return ema                                    # ER-IND-003-E

# ============================================================
# [ENGINE_RULE]
# [ER-IND-004] UTILS — ATR
# ============================================================
def _atr(candles: List[Candle], period: int) -> List[float]:
    """
    [ENGINE_RULE][ER-IND-004]
    """
    if period <= 0 or len(candles) < 2:
        return []                                  # ER-IND-004-A
    trs = []
    for i in range(1, len(candles)):
        h = candles[i].high
        l = candles[i].low
        pc = candles[i-1].close
        tr = max(h - l, abs(h - pc), abs(l - pc))
        trs.append(tr)                             # ER-IND-004-B
    atr = []
    for i, tr in enumerate(trs):
        if i == 0:
            atr.append(tr)                         # ER-IND-004-C
        else:
            atr.append((atr[-1] * (period - 1) + tr) / period)  # ER-IND-004-D
    return atr                                    # ER-IND-004-E

# ============================================================
# [ENGINE_RULE]
# [ER-IND-005] UTILS — SLOPE
# ============================================================
def _slope(series: List[float], lookback: int) -> List[float]:
    """
    [ENGINE_RULE][ER-IND-005]
    """
    if lookback <= 0 or len(series) <= lookback:
        return []                                  # ER-IND-005-A
    out = [0.0] * lookback
    for i in range(lookback, len(series)):
        out.append((series[i] - series[i - lookback]) / lookback)  # ER-IND-005-B
    return out                                    # ER-IND-005-C

# ============================================================
# [ENGINE_RULE]
# [ER-IND-006] INDICATOR COMPUTE (SINGLE ENTRY)
# ============================================================
def compute_indicators(candles: List[Candle], cfg: Dict) -> Dict[str, List[float]]:
    """
    [ENGINE_RULE][ER-IND-006]
    """
    out: Dict[str, List[float]] = {}

    closes = [c.close for c in candles]
    highs = [c.high for c in candles]
    lows = [c.low for c in candles]

    if cfg.get("IND_EMA_ENABLE", IND_CFG_DEFAULTS["IND_EMA_ENABLE"]):
        p = int(cfg.get("IND_EMA_PERIOD", IND_CFG_DEFAULTS["IND_EMA_PERIOD"]))
        out["EMA"] = _ema(closes, p)               # ER-IND-006-A

    if cfg.get("IND_ATR_ENABLE", IND_CFG_DEFAULTS["IND_ATR_ENABLE"]):
        p = int(cfg.get("IND_ATR_PERIOD", IND_CFG_DEFAULTS["IND_ATR_PERIOD"]))
        out["ATR"] = _atr(candles, p)              # ER-IND-006-B

    if cfg.get("IND_VOL_ENABLE", IND_CFG_DEFAULTS["IND_VOL_ENABLE"]):
        lb = int(cfg.get("IND_VOL_LOOKBACK", IND_CFG_DEFAULTS["IND_VOL_LOOKBACK"]))
        vols = []
        for i in range(len(candles)):
            if i < lb:
                vols.append(0.0)
            else:
                hh = max(highs[i-lb:i])
                ll = min(lows[i-lb:i])
                base = closes[i] if closes[i] != 0 else 1.0
                vols.append((hh - ll) / base * 100.0)
        out["VOL"] = vols                          # ER-IND-006-C

    if cfg.get("IND_SLOPE_ENABLE", IND_CFG_DEFAULTS["IND_SLOPE_ENABLE"]):
        lb = int(cfg.get("IND_SLOPE_LOOKBACK", IND_CFG_DEFAULTS["IND_SLOPE_LOOKBACK"]))
        if "EMA" in out and out["EMA"]:
            out["SLOPE"] = _slope(out["EMA"], lb)  # ER-IND-006-D
        else:
            out["SLOPE"] = []                      # ER-IND-006-E

    return out                                    # ER-IND-006-F

# ============================================================
# [ENGINE_RULE]
# [ER-IND-007] HELPERS — LAST VALUE
# ============================================================
def last(ind: Dict[str, List[float]], key: str):
    """
    [ENGINE_RULE][ER-IND-007]
    """
    arr = ind.get(key, [])
    return arr[-1] if arr else None                # ER-IND-007-A



# ============================================================
# [ENGINE_RULE]
# [ER-STATE-002] STATE COMPUTATION
# ============================================================
def compute_market_state(candles, ema_series, cfg):
    """
    [ENGINE_RULE][ER-STATE-002]
    OUTPUT:
      - "RANGE" | "TREND" | None
    """
    if not cfg.get("12_STATE_COOLDOWN_ENABLE", False):
        return None                              # ER-STATE-002-A

    lookback = cfg.get("10_ENTRY_LOOKBACK_BARS", 5)        # ER-STATE-002-B
    tol_pct = cfg.get("11_REENTRY_PRICE_TOL_PCT", 0.15) / 100.0  # ER-STATE-002-C

    if len(candles) < lookback + 1:
        return None                              # ER-STATE-002-D

    recent = candles[-lookback:]                # ER-STATE-002-E
    ema_recent = ema_series[-lookback:]         # ER-STATE-002-F

    crosses = 0
    for c, e in zip(recent, ema_recent):
        body_low = min(c.open, c.close)
        body_high = max(c.open, c.close)
        if body_low <= e <= body_high:
            crosses += 1                         # ER-STATE-002-G

    prices = [c.close for c in recent]          # ER-STATE-002-H
    max_p = max(prices)                          # ER-STATE-002-I
    min_p = min(prices)                          # ER-STATE-002-J
    drift = (max_p - min_p) / prices[-1]        # ER-STATE-002-K

    if crosses >= (lookback // 2) and drift <= tol_pct:
        return "RANGE"                           # ER-STATE-002-L

    return "TREND"                               # ER-STATE-002-M

# ============================================================
# [ENGINE_RULE]
# [ER-STATE-003] STATE UPDATE (SINGLE BAR)
# ============================================================
def state_module_step(candles, ema_series, state, cfg):
    """
    [ENGINE_RULE][ER-STATE-003]
    - 상태 라벨을 state.market_state에 기록
    """
    label = compute_market_state(candles, ema_series, cfg)
    if label is not None:
        state.market_state = label               # ER-STATE-003-A



# ============================================================
# STATE_MANAGER — V4 (STATE / PERSISTENCE ONLY)
# ENGINE_RULE / HUMAN_NOTE SPLIT TEMPLATE
# ============================================================

import os, json, tempfile
from dataclasses import dataclass, asdict
from typing import Optional

# ============================================================
# [ENGINE_RULE]
# [ER-STATE-001] STATE SCHEMA (FACTS ONLY)
# ============================================================
@dataclass
class EngineState:
    # --- Engine run facts ---
    version: str = "V4"                 # ER-STATE-001-A
    last_update_ts: int = 0             # ER-STATE-001-B

    # --- Position facts ---
    has_position: bool = False          # ER-STATE-001-C
    symbol: str = ""                    # ER-STATE-001-D
    side: str = ""                      # ER-STATE-001-E
    entry_price: float = 0.0            # ER-STATE-001-F
    qty: float = 0.0                    # ER-STATE-001-G

    # --- Exit progress facts ---
    tp1_done: bool = False              # ER-STATE-001-H
    trailing_active: bool = False       # ER-STATE-001-I
    trailing_low: Optional[float] = None    # ER-STATE-001-J
    trailing_stop: Optional[float] = None   # ER-STATE-001-K

    # --- Anti-spam facts ---
    bars_since_last_entry: int = 999999 # ER-STATE-001-L
    bars_since_last_exit: int = 999999  # ER-STATE-001-M
    entries_today: int = 0              # ER-STATE-001-N
    entries_in_cycle: int = 0           # ER-STATE-001-O

    # --- Candidate facts ---
    cand_active: bool = False           # ER-STATE-001-P
    cand_reason: str = ""               # ER-STATE-001-Q
    cand_price: float = 0.0             # ER-STATE-001-R
    cand_ts: int = 0                    # ER-STATE-001-S
    cand_birth_bar_id: str = ""         # ER-STATE-001-T

    # --- Market state label ---
    market_state: str = ""              # ER-STATE-001-U

# ============================================================
# [ENGINE_RULE]
# [ER-STATE-002] ATOMIC SAVE / LOAD
# ============================================================
def save_state_atomic(path: str, state: EngineState):
    """
    [ENGINE_RULE][ER-STATE-002]
    - 임시 파일 → os.replace (atomic)
    """
    d = asdict(state)                               # ER-STATE-002-A
    tmp_dir = os.path.dirname(path) or "."          # ER-STATE-002-B
    os.makedirs(tmp_dir, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(
        prefix="state_", suffix=".json", dir=tmp_dir
    )                                               # ER-STATE-002-C
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)                  # ER-STATE-002-D
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)                 # ER-STATE-002-E
        except Exception:
            pass


def load_state(path: str) -> EngineState:
    """
    [ENGINE_RULE][ER-STATE-003]
    - 파일 없으면 기본 상태
    - 누락 키는 기본값 복구
    """
    if not os.path.exists(path):
        return EngineState()                         # ER-STATE-003-A

    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return EngineState()                         # ER-STATE-003-B

    base = asdict(EngineState())                     # ER-STATE-003-C
    base.update({k: v for k, v in d.items() if k in base})
    return EngineState(**base)                       # ER-STATE-003-D

# ============================================================
# [ENGINE_RULE]
# [ER-STATE-004] STATE TRANSITIONS (FACT UPDATES ONLY)
# ============================================================
def on_entry_filled(
    state: EngineState,
    symbol: str,
    side: str,
    entry_price: float,
    qty: float,
    now_ts: int
):
    """
    [ENGINE_RULE][ER-STATE-004]
    """
    state.last_update_ts = now_ts                    # ER-STATE-004-A
    state.has_position = True                        # ER-STATE-004-B
    state.symbol = symbol                            # ER-STATE-004-C
    state.side = side                                # ER-STATE-004-D
    state.entry_price = float(entry_price)           # ER-STATE-004-E
    state.qty = float(qty)                           # ER-STATE-004-F

    state.tp1_done = False                           # ER-STATE-004-G
    state.trailing_active = False                    # ER-STATE-004-H
    state.trailing_low = None                        # ER-STATE-004-I
    state.trailing_stop = None                       # ER-STATE-004-J

    state.bars_since_last_entry = 0                  # ER-STATE-004-K
    state.entries_today += 1                         # ER-STATE-004-L
    state.entries_in_cycle += 1                      # ER-STATE-004-M

    clear_candidate(state)                           # ER-STATE-004-N


def on_tp1_done(state: EngineState, tp1_qty: float, now_ts: int):
    """
    [ENGINE_RULE][ER-STATE-005]
    """
    state.last_update_ts = now_ts                    # ER-STATE-005-A
    state.tp1_done = True                            # ER-STATE-005-B
    state.qty = max(0.0, float(state.qty) - float(tp1_qty))  # ER-STATE-005-C


def on_exit_done(state: EngineState, now_ts: int):
    """
    [ENGINE_RULE][ER-STATE-006]
    """
    state.last_update_ts = now_ts                    # ER-STATE-006-A
    state.has_position = False                       # ER-STATE-006-B
    state.entry_price = 0.0                          # ER-STATE-006-C
    state.qty = 0.0                                  # ER-STATE-006-D

    state.tp1_done = False                           # ER-STATE-006-E
    state.trailing_active = False                    # ER-STATE-006-F
    state.trailing_low = None                        # ER-STATE-006-G
    state.trailing_stop = None                       # ER-STATE-006-H

    state.bars_since_last_exit = 0                   # ER-STATE-006-I
    state.entries_in_cycle = 0                       # ER-STATE-006-J

    clear_candidate(state)                           # ER-STATE-006-K


def clear_candidate(state: EngineState):
    """
    [ENGINE_RULE][ER-STATE-007]
    """
    state.cand_active = False                        # ER-STATE-007-A
    state.cand_reason = ""                           # ER-STATE-007-B
    state.cand_price = 0.0                           # ER-STATE-007-C
    state.cand_ts = 0                                # ER-STATE-007-D
    state.cand_birth_bar_id = ""                     # ER-STATE-007-E


def register_candidate(
    state: EngineState,
    reason: str,
    price: float,
    ts: int,
    birth_bar_id: str,
    now_ts: int
):
    """
    [ENGINE_RULE][ER-STATE-008]
    """
    state.last_update_ts = now_ts                    # ER-STATE-008-A
    state.cand_active = True                         # ER-STATE-008-B
    state.cand_reason = reason                       # ER-STATE-008-C
    state.cand_price = float(price)                  # ER-STATE-008-D
    state.cand_ts = int(ts)                          # ER-STATE-008-E
    state.cand_birth_bar_id = birth_bar_id           # ER-STATE-008-F

# ============================================================
# [ENGINE_RULE]
# [ER-STATE-009] PERIODIC COUNTER TICK
# ============================================================
def on_new_bar_tick(state: EngineState, now_ts: int):
    """
    [ENGINE_RULE][ER-STATE-009]
    """
    state.last_update_ts = now_ts                    # ER-STATE-009-A
    state.bars_since_last_entry += 1                 # ER-STATE-009-B
    state.bars_since_last_exit += 1                  # ER-STATE-009-C



# ============================================================
# [ENGINE_RULE]
# [ER-ENTRY-001] CFG — ENTRY RELATED
# ============================================================
CFG = {
    # --- Candidate Generation ---
    "ENTRY_CANDIDATE_ENABLE": True,        # ER-ENTRY-001-A
    "EMA_PERIOD": 9,                       # ER-ENTRY-001-B

    # --- Cooldown Controls ---
    "ENTRY_COOLDOWN_BARS": 0,              # ER-ENTRY-001-C
    "REENTRY_SAME_REASON_BLOCK": True,     # ER-ENTRY-001-D
    "ENTRY_LOOKBACK_BARS": 5,              # ER-ENTRY-001-E

    # --- State-based Cooldown ---
    "COOLDOWN_RANGE_BARS": 4,              # ER-ENTRY-001-F
    "COOLDOWN_TREND_BARS": 1,              # ER-ENTRY-001-G
}

# ============================================================
# [ENGINE_RULE]
# [ER-ENTRY-002] ENTRY CANDIDATE — CORE
# ============================================================
def is_entry_candidate(candle, ema_value):
    """
    [ENGINE_RULE][ER-ENTRY-002]
    """
    body_low = min(candle.open, candle.close)   # ER-ENTRY-002-A
    return body_low < ema_value                 # ER-ENTRY-002-B

# ============================================================
# [ENGINE_RULE]
# [ER-ENTRY-003] ENTRY EXECUTION GATE
# ============================================================
def can_execute_entry(state, cfg):
    """
    [ENGINE_RULE][ER-ENTRY-003]
    """
    if state.bars_since_last_entry < cfg["ENTRY_COOLDOWN_BARS"]:
        return False                            # ER-ENTRY-003-A

    if cfg["REENTRY_SAME_REASON_BLOCK"]:
        if state.is_same_reason_within(cfg["ENTRY_LOOKBACK_BARS"]):
            return False                        # ER-ENTRY-003-B

    return True                                 # ER-ENTRY-003-C

# ============================================================
# [ENGINE_RULE]
# [ER-ENTRY-004] ENTRY FLOW
# ============================================================
def entry_flow(candle, ema_value, state, cfg):
    """
    [ENGINE_RULE][ER-ENTRY-004]
    """
    if not cfg["ENTRY_CANDIDATE_ENABLE"]:
        return                                 # ER-ENTRY-004-A

    if is_entry_candidate(candle, ema_value):
        state.register_candidate(
            reason="EMA_BODY_BELOW"
        )                                      # ER-ENTRY-004-B

    if state.has_candidate():
        if can_execute_entry(state, cfg):
            state.execute_entry()              # ER-ENTRY-004-C
            state.reset_candidate()            # ER-ENTRY-004-D


# ============================================================
# [ENGINE_RULE]
# [ER-EXEC-002] EXECUTION CFG DEFAULTS (MINIMAL)
# ============================================================
EXEC_CFG_DEFAULTS = {
    "EXEC_ENABLE": True,            # ER-EXEC-002-A
    "EXEC_RETRY_ENABLE": True,      # ER-EXEC-002-B
    "EXEC_RETRY_MAX": 3,            # ER-EXEC-002-C
    "EXEC_RETRY_SLEEP_SEC": 1.0,    # ER-EXEC-002-D
    "EXEC_TIMEOUT_SEC": 10.0,       # ER-EXEC-002-E
}

# ============================================================
# [ENGINE_RULE]
# [ER-EXEC-003] ORDER REQUEST STRUCT
# ============================================================
class OrderRequest:
    """
    [ENGINE_RULE][ER-EXEC-003]
    - 실행에 필요한 최소 정보만 포함
    """
    def __init__(self, symbol_info, side, qty, order_type="MARKET", reduce_only=False, client_id=None):
        self.symbol_info = symbol_info     # ER-EXEC-003-A
        self.side = side                   # ER-EXEC-003-B
        self.qty = qty                     # ER-EXEC-003-C
        self.order_type = order_type       # ER-EXEC-003-D
        self.reduce_only = reduce_only     # ER-EXEC-003-E
        self.client_id = client_id         # ER-EXEC-003-F

# ============================================================
# [ENGINE_RULE]
# [ER-EXEC-004] ORDER RESULT STRUCT
# ============================================================
class OrderResult:
    """
    [ENGINE_RULE][ER-EXEC-004]
    - 거래소 응답 정규화
    """
    def __init__(self, ok, order_id=None, executed_qty=None, avg_price=None, err=None, raw=None):
        self.ok = ok                       # ER-EXEC-004-A
        self.order_id = order_id           # ER-EXEC-004-B
        self.executed_qty = executed_qty   # ER-EXEC-004-C
        self.avg_price = avg_price         # ER-EXEC-004-D
        self.err = err                     # ER-EXEC-004-E
        self.raw = raw                     # ER-EXEC-004-F

# ============================================================
# [ENGINE_RULE]
# [ER-EXEC-005] EXECUTION CORE
# ============================================================
def place_order(exchange, req: OrderRequest, cfg, state=None):
    """
    [ENGINE_RULE][ER-EXEC-005]
    - 주문 실행: 요청 → 거래소 → 결과
    - 판단 금지
    """
    exec_enable = cfg.get("EXEC_ENABLE", EXEC_CFG_DEFAULTS["EXEC_ENABLE"])
    if not exec_enable:
        return OrderResult(ok=False, err="EXEC_DISABLED")   # ER-EXEC-005-A

    retry_enable = cfg.get("EXEC_RETRY_ENABLE", EXEC_CFG_DEFAULTS["EXEC_RETRY_ENABLE"])
    retry_max = int(cfg.get("EXEC_RETRY_MAX", EXEC_CFG_DEFAULTS["EXEC_RETRY_MAX"]))
    retry_sleep = float(cfg.get("EXEC_RETRY_SLEEP_SEC", EXEC_CFG_DEFAULTS["EXEC_RETRY_SLEEP_SEC"]))
    timeout_sec = float(cfg.get("EXEC_TIMEOUT_SEC", EXEC_CFG_DEFAULTS["EXEC_TIMEOUT_SEC"]))

    symbol = req.symbol_info.base        # ER-EXEC-005-B
    market = req.symbol_info.market      # ER-EXEC-005-C

    attempts = 0
    last_err = None

    while True:
        attempts += 1
        try:
            raw = exchange.create_order(
                symbol=symbol,           # ER-EXEC-005-D
                market=market,           # ER-EXEC-005-E
                side=req.side,            # ER-EXEC-005-F
                qty=req.qty,              # ER-EXEC-005-G
                order_type=req.order_type,# ER-EXEC-005-H
                reduce_only=req.reduce_only, # ER-EXEC-005-I
                client_id=req.client_id,  # ER-EXEC-005-J
                timeout_sec=timeout_sec,  # ER-EXEC-005-K
            )

            order_id = raw.get("orderId") or raw.get("id")            # ER-EXEC-005-L
            executed_qty = raw.get("executedQty") or raw.get("executed_qty")  # ER-EXEC-005-M
            avg_price = raw.get("avgPrice") or raw.get("avg_price")   # ER-EXEC-005-N

            if state is not None and hasattr(state, "log_execution"):
                state.log_execution(req, raw)                          # ER-EXEC-005-O

            return OrderResult(
                ok=True,
                order_id=order_id,
                executed_qty=executed_qty,
                avg_price=avg_price,
                raw=raw,
            )

        except Exception as e:
            last_err = str(e)                                           # ER-EXEC-005-P

            if state is not None and hasattr(state, "log_execution_error"):
                state.log_execution_error(req, last_err, attempts)     # ER-EXEC-005-Q

            if (not retry_enable) or (attempts >= retry_max):
                return OrderResult(ok=False, err=last_err)             # ER-EXEC-005-R

            import time
            time.sleep(retry_sleep)                                     # ER-EXEC-005-S

# ============================================================
# [ENGINE_RULE]
# [ER-EXEC-006] REDUCE-ONLY EXIT WRAPPER
# ============================================================
def place_reduce_only(exchange, symbol_info, side, qty, cfg, state=None, client_id=None):
    """
    [ENGINE_RULE][ER-EXEC-006]
    """
    req = OrderRequest(
        symbol_info=symbol_info,        # ER-EXEC-006-A
        side=side,                      # ER-EXEC-006-B
        qty=qty,                        # ER-EXEC-006-C
        order_type="MARKET",            # ER-EXEC-006-D
        reduce_only=True,               # ER-EXEC-006-E
        client_id=client_id             # ER-EXEC-006-F
    )
    return place_order(exchange, req, cfg, state)  # ER-EXEC-006-G


# ============================================================
# RECONCILER — V4 (POSITION SYNC / REALITY CHECK)
# ENGINE_RULE / HUMAN_NOTE SPLIT TEMPLATE
# ============================================================

from dataclasses import dataclass
from typing import Optional, Dict, Any

# ============================================================
# [ENGINE_RULE]
# [ER-REC-001] RECONCILE CFG DEFAULTS (READ-ONLY)
# ============================================================
REC_CFG_DEFAULTS = {
    "REC_ENABLE": True,                 # ER-REC-001-A
    "REC_ON_MISMATCH": "HALT",          # ER-REC-001-B
    "REC_ALLOW_SMALL_QTY_DIFF": True,   # ER-REC-001-C
    "REC_QTY_DIFF_TOL": 0.0001,         # ER-REC-001-D
    "REC_PRICE_DIFF_TOL_PCT": 0.10,     # ER-REC-001-E
    "REC_EVERY_SEC": 5,                 # ER-REC-001-F
}

# ============================================================
# [ENGINE_RULE]
# [ER-REC-002] RESULT STRUCT
# ============================================================
@dataclass
class ReconcileResult:
    ok: bool                             # ER-REC-002-A
    action: str = ""                    # ER-REC-002-B
    reason: str = ""                    # ER-REC-002-C
    meta: Optional[Dict[str, Any]] = None  # ER-REC-002-D

# ============================================================
# [ENGINE_RULE]
# [ER-REC-003] HELPERS
# ============================================================
def _pct_diff(a: float, b: float) -> float:
    if a == 0:
        return 0.0                      # ER-REC-003-A
    return abs(a - b) / abs(a) * 100.0  # ER-REC-003-B


def _qty_close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol            # ER-REC-003-C

# ============================================================
# [ENGINE_RULE]
# [ER-REC-004] EXCHANGE POSITION ADAPTER (MIN)
# ============================================================
class ExchangePositionAdapter:
    """
    [ENGINE_RULE][ER-REC-004]
    """
    def get_position(self, symbol: str) -> dict:
        raise NotImplementedError       # ER-REC-004-A

# ============================================================
# [ENGINE_RULE]
# [ER-REC-005] RECONCILER CORE
# ============================================================
class Reconciler:
    """
    [ENGINE_RULE][ER-REC-005]
    """
    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = {**REC_CFG_DEFAULTS, **(cfg or {})}  # ER-REC-005-A
        self._last_ts = 0.0                             # ER-REC-005-B

    def should_run(self) -> bool:
        import time
        every = float(self.cfg.get("REC_EVERY_SEC", REC_CFG_DEFAULTS["REC_EVERY_SEC"]))  # ER-REC-005-C
        now = time.time()
        if (now - self._last_ts) >= every:
            self._last_ts = now                         # ER-REC-005-D
            return True
        return False                                    # ER-REC-005-E

    def reconcile(self, symbol_info, state, exchange: ExchangePositionAdapter, execution=None) -> ReconcileResult:
        """
        [ENGINE_RULE][ER-REC-006]
        """
        if not self.cfg.get("REC_ENABLE", True):
            return ReconcileResult(ok=True)             # ER-REC-006-A

        if not self.should_run():
            return ReconcileResult(ok=True)             # ER-REC-006-B

        symbol = symbol_info.base                        # ER-REC-006-C
        ex = exchange.get_position(symbol)               # ER-REC-006-D

        ex_has = bool(ex.get("has_position", False))     # ER-REC-006-E
        ex_side = ex.get("side", "")                     # ER-REC-006-F
        ex_qty = float(ex.get("qty", 0.0))               # ER-REC-006-G
        ex_entry = float(ex.get("entry_price", 0.0))     # ER-REC-006-H

        st_has = bool(getattr(state, "has_position", False))  # ER-REC-006-I
        st_side = getattr(state, "side", "")             # ER-REC-006-J
        st_qty = float(getattr(state, "qty", 0.0) or 0.0)# ER-REC-006-K
        st_entry = float(getattr(state, "entry_price", 0.0) or 0.0)  # ER-REC-006-L

        qty_tol = float(self.cfg.get("REC_QTY_DIFF_TOL", REC_CFG_DEFAULTS["REC_QTY_DIFF_TOL"]))  # ER-REC-006-M
        price_tol_pct = float(self.cfg.get("REC_PRICE_DIFF_TOL_PCT", REC_CFG_DEFAULTS["REC_PRICE_DIFF_TOL_PCT"]))  # ER-REC-006-N

        same_has = (ex_has == st_has)                    # ER-REC-006-O
        same_side = (ex_side == st_side) if ex_has and st_has else True  # ER-REC-006-P
        same_qty = _qty_close(ex_qty, st_qty, qty_tol) if (ex_has and st_has) else True  # ER-REC-006-Q
        same_price = (_pct_diff(ex_entry, st_entry) <= price_tol_pct) if (ex_has and st_has and ex_entry > 0 and st_entry > 0) else True  # ER-REC-006-R

        if same_has and same_side and same_qty and same_price:
            return ReconcileResult(ok=True)              # ER-REC-006-S

        policy = str(self.cfg.get("REC_ON_MISMATCH", "HALT")).upper()  # ER-REC-006-T

        meta = {
            "symbol": {"raw": getattr(symbol_info, "raw", ""), "base": symbol_info.base, "market": getattr(symbol_info, "market", "")},
            "ex": {"has": ex_has, "side": ex_side, "qty": ex_qty, "entry": ex_entry},
            "st": {"has": st_has, "side": st_side, "qty": st_qty, "entry": st_entry},
            "policy": policy,
        }                                               # ER-REC-006-U

        if policy == "HALT":
            setattr(state, "halt_reason", "REC_MISMATCH")  # ER-REC-006-V
            setattr(state, "halted", True)                 # ER-REC-006-W
            return ReconcileResult(ok=False, action="HALT", reason="REC_MISMATCH", meta=meta)

        if policy == "STATE_FIX":
            state.has_position = ex_has                   # ER-REC-006-X
            state.side = ex_side if ex_has else ""         # ER-REC-006-Y
            state.qty = ex_qty if ex_has else 0.0          # ER-REC-006-Z
            state.entry_price = ex_entry if ex_has else 0.0  # ER-REC-006-AA
            state.tp1_done = False                         # ER-REC-006-AB
            state.trailing_active = False                  # ER-REC-006-AC
            state.trailing_low = None                      # ER-REC-006-AD
            state.trailing_stop = None                     # ER-REC-006-AE
            return ReconcileResult(ok=False, action="STATE_FIXED", reason="REC_STATE_FIXED", meta=meta)

        if policy == "FORCE_EXIT":
            if ex_has and execution is not None:
                exit_side = "BUY" if ex_side == "SHORT" else "SELL"  # ER-REC-006-AF
                res = execution.place_reduce_only(
                    exchange=state.exchange,
                    symbol_info=symbol_info,
                    side=exit_side,
                    qty=ex_qty,
                    cfg=getattr(state, "exec_cfg", {}),
                    state=state,
                    client_id="REC_FORCE_EXIT"
                )                                           # ER-REC-006-AG
                if getattr(res, "ok", False):
                    state.has_position = False              # ER-REC-006-AH
                    state.qty = 0.0                         # ER-REC-006-AI
                    state.entry_price = 0.0                # ER-REC-006-AJ
                    return ReconcileResult(ok=False, action="FORCE_EXIT_SENT", reason="REC_FORCE_EXIT_OK", meta=meta)
                return ReconcileResult(ok=False, action="FORCE_EXIT_SENT", reason="REC_FORCE_EXIT_FAIL", meta=meta)

            return ReconcileResult(ok=False, action="HALT", reason="REC_FORCE_EXIT_NO_EXEC", meta=meta)

        setattr(state, "halt_reason", "REC_POLICY_UNKNOWN")  # ER-REC-006-AK
        setattr(state, "halted", True)                       # ER-REC-006-AL
        return ReconcileResult(ok=False, action="HALT", reason="REC_POLICY_UNKNOWN", meta=meta)



# ============================================================
# [ENGINE_RULE]
# [ER-RISK-001] RISK CFG DEFAULTS (READ-ONLY)
# ============================================================
RISK_CFG_DEFAULTS = {
    "RISK_GUARD_ENABLE": True,        # ER-RISK-001-A
    "ENGINE_ENABLE": True,            # ER-RISK-001-B
    "HALT_MANUAL": False,             # ER-RISK-001-C
    "DATA_STALE_BLOCK": True,         # ER-RISK-001-D
    "MAX_ENTRIES_PER_DAY": 6,         # ER-RISK-001-E
    "CAPITAL_BASE_USDT": 200.0,       # ER-RISK-001-F
    "CAPITAL_MAX_LOSS_PCT": 100.0,    # ER-RISK-001-G
}

# ============================================================
# [ENGINE_RULE]
# [ER-RISK-002] RESULT STRUCT
# ============================================================
class RiskDecision:
    """
    [ENGINE_RULE][ER-RISK-002]
    """
    def __init__(self, ok: bool, reason: str = ""):
        self.ok = ok                  # ER-RISK-002-A
        self.reason = reason          # ER-RISK-002-B

# ============================================================
# [ENGINE_RULE]
# [ER-RISK-003] ENGINE / OPS CHECK
# ============================================================
def _check_engine(cfg) -> RiskDecision:
    if not cfg.get("ENGINE_ENABLE", True):
        return RiskDecision(False, "ENGINE_OFF")     # ER-RISK-003-A
    if cfg.get("HALT_MANUAL", False):
        return RiskDecision(False, "HALT_MANUAL")    # ER-RISK-003-B
    return RiskDecision(True)                         # ER-RISK-003-C

# ============================================================
# [ENGINE_RULE]
# [ER-RISK-004] DATA STALE CHECK
# ============================================================
def _check_data(feed, symbol: str, tf_list, cfg) -> RiskDecision:
    if not cfg.get("DATA_STALE_BLOCK", True):
        return RiskDecision(True)                     # ER-RISK-004-A
    for tf in tf_list:
        if feed.is_stale(symbol, tf):
            return RiskDecision(False, "DATA_STALE") # ER-RISK-004-B
    return RiskDecision(True)                         # ER-RISK-004-C

# ============================================================
# [ENGINE_RULE]
# [ER-RISK-005] FREQUENCY CHECK
# ============================================================
def _check_frequency(state, cfg) -> RiskDecision:
    if state.entries_today >= int(cfg.get("MAX_ENTRIES_PER_DAY", 0)):
        return RiskDecision(False, "MAX_ENTRIES_PER_DAY")  # ER-RISK-005-A
    return RiskDecision(True)                               # ER-RISK-005-B

# ============================================================
# [ENGINE_RULE]
# [ER-RISK-006] LOSS CONTROL CHECK
# ============================================================
def _check_loss(state, cfg) -> RiskDecision:
    """
    [ENGINE_RULE][ER-RISK-006]
    - 누적 손실률 한도 초과 여부
    - state에 기록된 '사실'만 사용
    """
    base = float(cfg.get("CAPITAL_BASE_USDT", 0.0))        # ER-RISK-006-A
    max_loss_pct = float(cfg.get("CAPITAL_MAX_LOSS_PCT", 100.0))  # ER-RISK-006-B

    realized_pnl = getattr(state, "realized_pnl_usdt", 0.0)  # ER-RISK-006-C

    if base <= 0:
        return RiskDecision(True)                          # ER-RISK-006-D

    loss_pct = (-realized_pnl / base) * 100.0 if realized_pnl < 0 else 0.0  # ER-RISK-006-E
    if loss_pct >= max_loss_pct:
        return RiskDecision(False, "MAX_LOSS_REACHED")     # ER-RISK-006-F

    return RiskDecision(True)                               # ER-RISK-006-G

# ============================================================
# [ENGINE_RULE]
# [ER-RISK-007] MAIN GATE
# ============================================================
def risk_guard_check(
    state,
    cfg,
    feed=None,
    symbol: str = "",
    tf_list=None,
) -> RiskDecision:
    """
    [ENGINE_RULE][ER-RISK-007]
    - ENTRY/EXIT 직전 호출
    """
    if not cfg.get("RISK_GUARD_ENABLE", True):
        return RiskDecision(True)                           # ER-RISK-007-A

    # 1) Engine / Ops
    r = _check_engine(cfg)                                  # ER-RISK-007-B
    if not r.ok:
        return r

    # 2) Data
    if feed is not None and tf_list:
        r = _check_data(feed, symbol, tf_list, cfg)        # ER-RISK-007-C
        if not r.ok:
            return r

    # 3) Frequency
    r = _check_frequency(state, cfg)                        # ER-RISK-007-D
    if not r.ok:
        return r

    # 4) Loss Control
    r = _check_loss(state, cfg)                             # ER-RISK-007-E
    if not r.ok:
        return r

    return RiskDecision(True)                               # ER-RISK-007-F



# ============================================================
# LOGGER_MODULE — V4 (EVENT / AUDIT LOG ONLY)
# ENGINE_RULE / HUMAN_NOTE SPLIT TEMPLATE
# ============================================================

import os, json, time
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

# ============================================================
# [ENGINE_RULE]
# [ER-LOG-001] LOGGER CFG (READ-ONLY)
# ============================================================
LOG_CFG_DEFAULTS = {
    "LOG_ENABLE": True,             # ER-LOG-001-A
    "LOG_PATH": "v4_events.jsonl",  # ER-LOG-001-B
    "LOG_FLUSH_EVERY": 1,           # ER-LOG-001-C
    "LOG_INCLUDE_RAW": False,       # ER-LOG-001-D
}

# ============================================================
# [ENGINE_RULE]
# [ER-LOG-002] EVENT TYPES (STANDARD)
# ============================================================
EVENT = {
    "ENGINE_START": "ENGINE_START",     # ER-LOG-002-A
    "ENGINE_TICK": "ENGINE_TICK",       # ER-LOG-002-B

    "CANDIDATE_ADD": "CANDIDATE_ADD",   # ER-LOG-002-C
    "CANDIDATE_CLEAR": "CANDIDATE_CLEAR",

    "ENTRY_EXEC": "ENTRY_EXEC",
    "ENTRY_FILLED": "ENTRY_FILLED",

    "EXIT_TP1": "EXIT_TP1",
    "EXIT_SL": "EXIT_SL",
    "EXIT_TRAIL": "EXIT_TRAIL",
    "EXIT_DONE": "EXIT_DONE",

    "RISK_BLOCK": "RISK_BLOCK",
    "DATA_STALE": "DATA_STALE",

    "EXEC_OK": "EXEC_OK",
    "EXEC_FAIL": "EXEC_FAIL",

    "STATE_SAVE": "STATE_SAVE",
    "STATE_LOAD": "STATE_LOAD",

    "ERROR": "ERROR",
}

# ============================================================
# [ENGINE_RULE]
# [ER-LOG-003] EVENT RECORD STRUCT
# ============================================================
@dataclass
class EventRecord:
    ts_ms: int                     # ER-LOG-003-A
    type: str                      # ER-LOG-003-B
    symbol: str = ""               # ER-LOG-003-C
    tf: str = ""                   # ER-LOG-003-D
    cid: str = ""                  # ER-LOG-003-E
    price: float = 0.0             # ER-LOG-003-F
    qty: float = 0.0               # ER-LOG-003-G
    reason: str = ""               # ER-LOG-003-H
    meta: Optional[Dict[str, Any]] = None  # ER-LOG-003-I
    raw: Optional[Dict[str, Any]] = None   # ER-LOG-003-J

# ============================================================
# [ENGINE_RULE]
# [ER-LOG-004] LOGGER CORE
# ============================================================
class EventLogger:
    """
    [ENGINE_RULE][ER-LOG-004]
    - JSONL append 전용
    - best-effort
    """
    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = {**LOG_CFG_DEFAULTS, **(cfg or {})}   # ER-LOG-004-A
        self.path = self.cfg["LOG_PATH"]                 # ER-LOG-004-B
        self.enable = bool(self.cfg["LOG_ENABLE"])       # ER-LOG-004-C
        self.flush_every = int(self.cfg["LOG_FLUSH_EVERY"])  # ER-LOG-004-D
        self.include_raw = bool(self.cfg["LOG_INCLUDE_RAW"]) # ER-LOG-004-E
        self._count = 0                                  # ER-LOG-004-F

        d = os.path.dirname(self.path)
        if d:
            os.makedirs(d, exist_ok=True)                # ER-LOG-004-G

        self._fh = None
        if self.enable:
            self._fh = open(self.path, "a", encoding="utf-8")  # ER-LOG-004-H

    def close(self):
        """
        [ENGINE_RULE][ER-LOG-005]
        """
        try:
            if self._fh:
                self._fh.flush()
                self._fh.close()
        except Exception:
            pass

    def log(self, rec: EventRecord):
        """
        [ENGINE_RULE][ER-LOG-006]
        - 이벤트 1건 기록
        """
        if not self.enable or not self._fh:
            return

        try:
            d = asdict(rec)                               # ER-LOG-006-A

            if not self.include_raw:
                d["raw"] = None                           # ER-LOG-006-B

            line = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
            self._fh.write(line + "\n")                   # ER-LOG-006-C
            self._count += 1                              # ER-LOG-006-D

            if self._count % self.flush_every == 0:
                self._fh.flush()                          # ER-LOG-006-E
        except Exception:
            pass                                          # ER-LOG-006-F

# ============================================================
# [ENGINE_RULE]
# [ER-LOG-007] TIME HELPER
# ============================================================
def now_ms():
    return int(time.time() * 1000)                        # ER-LOG-007-A

# ============================================================
# [ENGINE_RULE]
# [ER-LOG-008] EVENT FACTORY
# ============================================================
def make_event(
    etype: str,
    symbol: str = "",
    tf: str = "",
    cid: str = "",
    price: float = 0.0,
    qty: float = 0.0,
    reason: str = "",
    meta: Optional[Dict[str, Any]] = None,
    raw: Optional[Dict[str, Any]] = None,
) -> EventRecord:
    """
    [ENGINE_RULE][ER-LOG-008]
    - 표준 이벤트 생성
    """
    return EventRecord(
        ts_ms=now_ms(),                                  # ER-LOG-008-A
        type=etype,
        symbol=symbol,
        tf=tf,
        cid=cid,
        price=float(price) if price is not None else 0.0,
        qty=float(qty) if qty is not None else 0.0,
        reason=reason or "",
        meta=meta or None,
        raw=raw or None,
    )



# ============================================================
# TELEMETRY / HEALTH_MONITOR — V4 (LIVENESS / HEALTH ONLY)
# ENGINE_RULE / HUMAN_NOTE SPLIT TEMPLATE
# ============================================================

import os, json, time
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

# ============================================================
# [ENGINE_RULE]
# [ER-TEL-001] TELEMETRY CFG (READ-ONLY)
# ============================================================
TEL_CFG_DEFAULTS = {
    "TEL_ENABLE": True,                 # ER-TEL-001-A
    "TEL_PATH": "v4_health.json",       # ER-TEL-001-B
    "TEL_WRITE_EVERY_SEC": 5,           # ER-TEL-001-C
    "TEL_INCLUDE_STATE": False,         # ER-TEL-001-D
}

# ============================================================
# [ENGINE_RULE]
# [ER-TEL-002] HEALTH SNAPSHOT STRUCT
# ============================================================
@dataclass
class HealthSnapshot:
    ts_ms: int                          # ER-TEL-002-A
    engine_enable: bool                # ER-TEL-002-B
    status: str                        # ER-TEL-002-C  ("RUNNING"/"HALTED"/"ERROR")
    last_tick_ts_ms: int               # ER-TEL-002-D
    last_data_ts_ms: int               # ER-TEL-002-E
    last_entry_ts_ms: int              # ER-TEL-002-F
    last_exit_ts_ms: int               # ER-TEL-002-G
    error_count: int                   # ER-TEL-002-H
    last_error: str = ""               # ER-TEL-002-I
    meta: Optional[Dict[str, Any]] = None  # ER-TEL-002-J

# ============================================================
# [ENGINE_RULE]
# [ER-TEL-003] CORE MONITOR
# ============================================================
class HealthMonitor:
    """
    [ENGINE_RULE][ER-TEL-003]
    - 헬스 스냅샷을 파일로 주기적 기록
    - overwrite 방식 (항상 최신 1개)
    """
    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = {**TEL_CFG_DEFAULTS, **(cfg or {})}   # ER-TEL-003-A
        self.enable = bool(self.cfg["TEL_ENABLE"])       # ER-TEL-003-B
        self.path = self.cfg["TEL_PATH"]                 # ER-TEL-003-C
        self.write_every_sec = float(self.cfg["TEL_WRITE_EVERY_SEC"])  # ER-TEL-003-D
        self.include_state = bool(self.cfg["TEL_INCLUDE_STATE"])       # ER-TEL-003-E

        self._last_write_ts = 0.0                         # ER-TEL-003-F

        d = os.path.dirname(self.path)
        if d:
            os.makedirs(d, exist_ok=True)                 # ER-TEL-003-G

    def _now_ms(self) -> int:
        return int(time.time() * 1000)                    # ER-TEL-003-H

    def update(
        self,
        cfg: Dict[str, Any],
        state,
        status: str,
        last_data_ts_ms: int,
        last_error: str = "",
        meta: Optional[Dict[str, Any]] = None,
    ):
        """
        [ENGINE_RULE]
        [ER-TEL-004]
        - 상태 업데이트 요청
        - write cadence 충족 시에만 파일 갱신
        """
        if not self.enable:
            return                                        # ER-TEL-004-A

        now = self._now_ms()
        if (time.time() - self._last_write_ts) < self.write_every_sec:
            return                                        # ER-TEL-004-B

        # --- state facts (없으면 0) ---
        last_tick = getattr(state, "last_update_ts", 0)   # ER-TEL-004-C
        last_entry = getattr(state, "last_entry_ts_ms", 0)
        last_exit = getattr(state, "last_exit_ts_ms", 0)
        error_count = getattr(state, "error_count", 0)

        snap = HealthSnapshot(
            ts_ms=now,
            engine_enable=bool(cfg.get("1_ENGINE_ENABLE", True)),  # ER-TEL-004-D
            status=status,
            last_tick_ts_ms=int(last_tick) if last_tick else now,
            last_data_ts_ms=int(last_data_ts_ms) if last_data_ts_ms else 0,
            last_entry_ts_ms=int(last_entry) if last_entry else 0,
            last_exit_ts_ms=int(last_exit) if last_exit else 0,
            error_count=int(error_count),
            last_error=last_error or "",
            meta=meta or None,
        )

        payload = asdict(snap)                             # ER-TEL-004-E

        # 옵션: state 포함
        if self.include_state:
            try:
                payload["state"] = state.__dict__          # ER-TEL-004-F
            except Exception:
                payload["state"] = None

        # overwrite write (atomic-ish)
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
                f.flush()
                os.fsync(f.fileno())
            self._last_write_ts = time.time()              # ER-TEL-004-G
        except Exception:
            pass                                           # ER-TEL-004-H



# ============================================================
# SCHEDULER / MAIN_LOOP — V4 (ORCHESTRATOR)
# ENGINE_RULE / HUMAN_NOTE SPLIT TEMPLATE
# ============================================================

import time
import traceback

# ============================================================
# [ENGINE_RULE]
# [ER-SCH-002] TIMEFRAME PLAN (FIXED SCHEDULING MAP)
# ============================================================
TF_PLAN = {
    # key: (timeframe, step_sec)
    "TF_ENTRY": ("5m", 2.0),   # ER-SCH-002-A
    "TF_EXIT":  ("3m", 2.0),   # ER-SCH-002-B
}

# ============================================================
# [ENGINE_RULE]
# [ER-SCH-003] SAFE CALL (NO CRASH, NO SWALLOW POLICY)
# ============================================================
def safe_call(fn, *args, **kwargs):
    """
    [ENGINE_RULE][ER-SCH-003]
    - 예외를 삼키지 않고, 루프를 유지
    - 실패는 반환값(Exception)으로 상위에서 인지 가능
    """
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return e

# ============================================================
# [ENGINE_RULE]
# [ER-SCH-004] SINGLE LOOP TICK (FIXED ORDER)
# ============================================================
def scheduler_tick(
    symbol: str,
    cfg: dict,
    feed,
    state,
    state_mgr,
    entry_engine,
    exit_engine,
    execution,
    state_labeler,
    ema_calc,
    now_ms: int,
):
    """
    [ENGINE_RULE][ER-SCH-004]
    - 단일 tick에서 수행되는 고정 순서
    """

    # [ER-SCH-004-0] DATA UPDATE (PER TF)
    for _, (tf, _) in TF_PLAN.items():
        safe_call(feed.poll_step, symbol, tf)

    # [ER-SCH-004-1] STALE CHECK (BLOCK ALL)
    for _, (tf, _) in TF_PLAN.items():
        if feed.is_stale(symbol, tf):
            return

    # [ER-SCH-004-2] STATE LABEL UPDATE (RANGE/TREND)
    tf_entry = TF_PLAN["TF_ENTRY"][0]
    candles_entry = feed.get_candles(symbol, tf_entry)
    ema_entry = ema_calc(candles_entry, cfg)
    safe_call(state_labeler.state_module_step, candles_entry, ema_entry, state, cfg)

    # [ER-SCH-004-3] ENTRY PIPELINE (ENTRY TF)
    if not state.has_position:
        last_candle = candles_entry[-1]
        last_ema = ema_entry[-1] if ema_entry else None
        if last_ema is not None:
            safe_call(entry_engine.entry_engine_step, last_candle, last_ema, state, cfg)

    # [ER-SCH-004-4] EXIT PIPELINE (EXIT TF)
    if state.has_position:
        tf_exit = TF_PLAN["TF_EXIT"][0]
        candles_exit = feed.get_candles(symbol, tf_exit)
        if candles_exit:
            last_price = candles_exit[-1].close
            safe_call(
                exit_engine.exit_engine_step,
                last_price,
                state,
                cfg,
                execution,
                symbol,
            )

    # [ER-SCH-004-5] STATE SAVE (ALWAYS)
    safe_call(state_mgr.save_state_atomic, cfg.get("STATE_FILE", "state.json"), state)

# ============================================================
# [ENGINE_RULE]
# [ER-SCH-005] MAIN LOOP (INFINITE)
# ============================================================
def run_main_loop(
    symbol: str,
    cfg: dict,
    feed,
    state,
    state_mgr,
    entry_engine,
    exit_engine,
    execution,
    state_labeler,
    ema_calc,
):
    """
    [ENGINE_RULE][ER-SCH-005]
    - 종료 조건 없이 단일 루프
    - sleep은 TF_PLAN 기준 최소 주기 사용
    """
    min_sleep = min(step for _, step in TF_PLAN.values())  # ER-SCH-005-A

    while True:
        now_ms = int(time.time() * 1000)  # ER-SCH-005-B
        try:
            scheduler_tick(
                symbol=symbol,
                cfg=cfg,
                feed=feed,
                state=state,
                state_mgr=state_mgr,
                entry_engine=entry_engine,
                exit_engine=exit_engine,
                execution=execution,
                state_labeler=state_labeler,
                ema_calc=ema_calc,
                now_ms=now_ms,
            )
        except Exception:
            # [ER-SCH-005-C] LAST RESORT: LOOP LIVES, STATE TRY SAVE
            traceback.print_exc()
            try:
                state_mgr.save_state_atomic(cfg.get("STATE_FILE", "state.json"), state)  # ER-SCH-005-D
            except Exception:
                pass

        time.sleep(min_sleep)  # ER-SCH-005-E

# ============================================================
# [BOOTSTRAP] MINIMAL (STEP 3-2)
# ============================================================

# --- SYMBOL ---
BOOT_SYMBOL = CFG.get("TRADE_SYMBOL") or CFG.get("0_TRADE_SYMBOL")

# --- STATE ---
state = EngineState()

# --- FEED ---
# --- FEED ---
cfg_mgr = CfgManager(CFG)
adapter = ExchangeDataAdapter()
feed = DataFeed(adapter, CFG)

# --- MANAGER / ENGINES (기준선 최소 조립) ---
state_mgr = Reconciler(CFG)

entry_engine = RiskDecision(CFG)
exit_engine  = RiskDecision(CFG)

execution = ExchangePositionAdapter()

state_labeler = EventLogger(CFG)

ema_calc = None

# --- SYMBOL INFO ---
symbol_info = SymbolInfo(
    raw=BOOT_SYMBOL,
    market=BOOT_SYMBOL,
    display=BOOT_SYMBOL,
    base=BOOT_SYMBOL,
)

feed.symbol_info = symbol_info



# ============================================================
# [SEED] MINIMAL CANDLE SEED (STEP 5-1)
# ============================================================

# 기본 TF 하나만 시드 (예: 1m)
SEED_TF = "1m"

# 빈 캔들 1개 생성 (현재 시각 기준)
now_ms = int(time.time() * 1000)

seed_candle = Candle(
    ts=now_ms,
    open=1.0,
    high=1.0,
    low=1.0,
    close=1.0,
    vol=0.0,
    is_closed=True,
)


# ============================================================
# [SEED] MINIMAL FEED STATE SEED (STEP 5-1) — SAFE MODE
# ============================================================

now_ms = int(time.time() * 1000)

# feed 내부에 last_ts 캐시가 없으면 생성
if not hasattr(feed, "last_ts"):
    feed.last_ts = {}

# 최소 TF 하나에 대해 현재 시각 기록
SEED_TF = "1m"
feed.last_ts[SEED_TF] = now_ms

# ============================================================
# [STEP 3-3] CONNECT MAIN LOOP (INTENTIONAL NEXT ERROR)
# ============================================================
run_main_loop(
    symbol=symbol_info,
    cfg=CFG,
    feed=feed,
    state=state,
    state_mgr=state_mgr,
    entry_engine=entry_engine,
    exit_engine=exit_engine,
    execution=execution,
    state_labeler=state_labeler,
    ema_calc=ema_calc,
)

# ============================================================
# [PROC-001] MAIN ENTRY — CONNECT MAIN LOOP (BLOCKING)
# ============================================================

if __name__ == "__main__":
    run_main_loop(
        symbol=symbol_info,
        cfg=CFG,
        feed=feed,
        state=state,
        state_mgr=state_mgr,
        entry_engine=entry_engine,
        exit_engine=exit_engine,
        execution=execution,
        state_labeler=state_labeler,
        ema_calc=ema_calc,
    )


