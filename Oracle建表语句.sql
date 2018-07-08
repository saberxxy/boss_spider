create table boss_job_list
(uuid varchar2(200),
page_num varchar(10),
keywords varchar2(20),
jobid varchar2(100),
job_detail_url varchar2(2000)
);
comment on table boss_job_list is 'boss直聘岗位链接表';
comment on column boss_job_list.uuid is '主键';
comment on column boss_job_list.page_num is '页数';
comment on column boss_job_list.keywords is '关键词';
comment on column boss_job_list.jobid is '岗位编号';
comment on column boss_job_list.job_detail_url is '岗位详细信息链接';
