import pandas as pd
import lightgbm as lgb
import pickle
def transform_to_dataframe(row):
    ohe_service = pickle.load(open(r'C:\Users\hp\Desktop\ppp\env\files\ohe_service.pkl','rb'))
    df = pd.DataFrame(columns=['id', 'srcip', 'dstip', 'sttl', 'dttl', 'service', 'swin', 'trans_depth', 'res_bdy_len',
                               'stime', 'sintpkt', 'dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports',
                               'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src',
                               'ct_dst_ltm', 'ct_src_ltm', 'ct_dst_sport_ltm', 'dur_log1p', 'sbytes_log1p',
                               'dbytes_log1p', 'sload_log1p', 'dload_log1p', 'spkts_log1p', 'stcpb_log1p',
                               'dtcpb_log1p', 'smeansz_log1p', 'dmeansz_log1p', 'sjit_log1p', 'djit_log1p',
                               'network_bytes_log1p', 'proto_3pc', 'proto_a_n', 'proto_aes_sp3_d', 'proto_any',
                               'proto_argus', 'proto_aris', 'proto_arp', 'proto_ax_25', 'proto_bbn_rcc', 'proto_bna',
                               'proto_br_sat_mon', 'proto_cbt', 'proto_cftp', 'proto_chaos', 'proto_compaq_peer',
                               'proto_cphb', 'proto_cpnx', 'proto_crtp', 'proto_crudp', 'proto_dcn', 'proto_ddp',
                               'proto_ddx', 'proto_dgp', 'proto_egp', 'proto_eigrp', 'proto_emcon', 'proto_encap',
                               'proto_esp', 'proto_etherip', 'proto_fc', 'proto_fire', 'proto_ggp', 'proto_gmtp',
                               'proto_gre', 'proto_hmp', 'proto_i_nlsp', 'proto_iatp', 'proto_ib', 'proto_icmp',
                               'proto_idpr', 'proto_idpr_cmtp', 'proto_idrp', 'proto_ifmp', 'proto_igmp', 'proto_igp',
                               'proto_il', 'proto_ip', 'proto_ipcomp', 'proto_ipcv', 'proto_ipip', 'proto_iplt',
                               'proto_ipnip', 'proto_ippc', 'proto_ipv6', 'proto_ipv6_frag', 'proto_ipv6_no',
                               'proto_ipv6_opts', 'proto_ipv6_route', 'proto_ipx_n_ip', 'proto_irtp', 'proto_isis',
                               'proto_iso_ip', 'proto_iso_tp4', 'proto_kryptolan', 'proto_l2tp', 'proto_larp',
                               'proto_leaf_1', 'proto_leaf_2', 'proto_merit_inp', 'proto_mfe_nsp', 'proto_mhrp',
                               'proto_micp', 'proto_mobile', 'proto_mtp', 'proto_mux', 'proto_narp', 'proto_netblt',
                               'proto_nsfnet_igp', 'proto_nvp', 'proto_ospf', 'proto_pgm', 'proto_pim', 'proto_pipe',
                               'proto_pnni', 'proto_pri_enc', 'proto_prm', 'proto_ptp', 'proto_pup', 'proto_pvp',
                               'proto_qnx', 'proto_rdp', 'proto_rsvp', 'proto_rtp', 'proto_rvd', 'proto_sat_expak',
                               'proto_sat_mon', 'proto_sccopmce', 'proto_scps', 'proto_sctp', 'proto_sdrp',
                               'proto_secure_vmtp', 'proto_sep', 'proto_skip', 'proto_sm', 'proto_smp', 'proto_snp',
                               'proto_sprite_rpc', 'proto_sps', 'proto_srp', 'proto_st2', 'proto_stp', 'proto_sun_nd',
                               'proto_swipe', 'proto_tcf', 'proto_tcp', 'proto_tlsp', 'proto_tp_plus', 'proto_trunk_1',
                               'proto_trunk_2', 'proto_ttp', 'proto_udp', 'proto_udt', 'proto_unas', 'proto_uti',
                               'proto_vines', 'proto_visa', 'proto_vmtp', 'proto_vrrp', 'proto_wb_expak',
                               'proto_wb_mon', 'proto_wsn', 'proto_xnet', 'proto_xns_idp', 'proto_xtp', 'proto_zero',
                               'state_ACC', 'state_CLO', 'state_CON', 'state_ECO', 'state_ECR', 'state_FIN', 'state_INT',
                               'state_MAS', 'state_PAR', 'state_REQ', 'state_RST', 'state_TST', 'state_TXD',
                               'state_URH', 'state_URN', 'state_no'])
    df.loc[0] = row
    df = df.drop(["id","srcip","dstip"], axis=1)
    print(df.shape)
    Xm = ohe_service.transform(df['service'].values.reshape(-1, 1))
    df= pd.concat([df,pd.DataFrame(Xm.toarray(), columns=['service_'+i for i in ohe_service.categories_[0]])],axis=1)
    print(df.shape)
    df.drop(["service"], axis=1,inplace=True)
    print(df.shape)
    return df

def prediction(row):
    df = transform_to_dataframe(row)
    model=lgb.Booster(model_file=r'C:\Users\hp\Desktop\ppp\env\files\lightgbm_model.txt')
    p=model.predict(df, num_iteration=model.best_iteration)
    if(p[0]>0.5):
        return "possible attaque"
    else:
        return "normal"
    