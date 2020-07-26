import time

from logging import INFO

from ScrapyUtils import core


from . import Command

def _detail_info(setting) -> str:
    """
    Args:
        setting:
    """
    prepare = 'Selected Prepare: {} - {}'.format(setting.CurrentPrepare.get_name(), str(setting.CurrentPrepare))
    model = core.components_detail(setting.CurrentModels, 'Model')
    scheme = core.components_detail(setting.CurrentSchemeList, 'Scheme')
    processor = core.components_detail(setting.CurrentProcessorsList, 'Processor')
    return '\n'.join([model, scheme, processor])


def _base_info(setting) -> str:
    """
    Args:
        setting:
    """
    target = 'target name: {}'.format(setting.Target)
    thread = 'thread: {}'.format(base.command.commands.thread)

    ProxyAble = setting.ProxyAble
    ProxyURL = setting.ProxyURL
    proxy_able = 'proxy able: {}'.format(ProxyAble)
    proxy_url = 'proxy from: {}'.format(ProxyURL)

    block = 'process task block: {}'.format(setting.Block)
    failed_block = 'process task failed block: {}'.format(setting.FailedBlock)
    dump_limit = 'dump limit: {}'.format(setting.DumpLimit)

    proxy = proxy_able if not setting.ProxyAble else '\n'.join([proxy_able, proxy_url])

    return (target, thread, proxy, block, failed_block, dump_limit)


class Check(Command):
    require_target = True

    @property
    def syntax(self):
        return '[Check]'

    def _run(self):
        setting = self.setting

        time.sleep(1)
        schemes = [str(x) for x in setting.SchemeList]

        current_schemes = [str(x) for x in setting.CurrentSchemeList]

        self.log(msg='setting schemes: \n\t' + '\n\t'.join(schemes), level=INFO)

        self.log(msg='current schemes: \n\t' + '\n\t'.join(current_schemes), level=INFO)
        time.sleep(1)

        current_models = [str(x) for x in setting.CurrentModels]

        self.log(msg='current models: \n\t' + '\n\t'.join(current_models), level=INFO)

        processors = [str(x) for x in setting.ProcessorList]
        time.sleep(1)

        current_processors = [str(x) for x in setting.CurrentProcessorsList]

        self.log(msg='setting processor: \n\t' + '\n\t'.join(processors), level=INFO)

        self.log(msg='current processor: \n\t' + '\n\t'.join(current_processors), level=INFO)
        time.sleep(1)

        start = time.time()
        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, base.command.commands.thread)

        # comment this
        time.sleep(1)
        end = time.time()

        self.log('spend %.2f second(s) in' % float(end - start))

    def run(self):
        setting = self.setting

        # self.log('Target: {}'.format(self.target))
        # self.log('Thread: {}'.format(self.setting.Thread))
        # self.log('ProxyAble: {}\n'.format(self.setting.ProxyAble))
        time.sleep(0.5)
        # self.log('Target base info:')
        [self.log(x) for x in _base_info(setting)]
        time.sleep(1.2)

        self.log('Activated Components:\n' + _detail_info(setting))
        start = time.time()
        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, base.command.commands.thread)

        self.log('spend %.2f second(s) in' % float(time.time() - start))

        [scraper._quit() for scraper in scrapers]
