from psireporter.plugin import ReporterPlugin, OutputPlugin, PluginRegistry, PLUGIN_TYPE_OUTPUT, RegisterPlugin, PLUGIN_TYPE_REPORTER, Report
from psireporter.worker import OutputManager
import time
import asyncio

@RegisterPlugin(plugin_id="outputter-one", plugin_name="outputter-one", plugin_type=PLUGIN_TYPE_OUTPUT)
class OutputOne(OutputPlugin):
    def send(self, report):
        time.sleep(1)
        print("[%s] processed report - ID: %s - Message: %s - Timestamp: %s" % (self.PLUGIN_NAME, report.id, report.message, report.timestamp))
        return True
        

@RegisterPlugin(plugin_id="outputter-two", plugin_name="outputter-two", plugin_type=PLUGIN_TYPE_OUTPUT)
class OutputTwo(OutputPlugin):
    def send(self, report):
        time.sleep(3)
        print("[%s] processed report - ID: %s - Message: %s - Timestamp: %s" % (self.PLUGIN_NAME, report.id, report.message, report.timestamp))
        return True


@RegisterPlugin(plugin_id="reporter-one", plugin_name="Reporter One", plugin_type=PLUGIN_TYPE_REPORTER)
class ReporterOne(ReporterPlugin):
    def report(self):
        return Report(message="ReporterOne says Hello World!")


outputters = [cls({}) for cls in PluginRegistry.Get().get_all_plugins(PLUGIN_TYPE_OUTPUT).values()]

om = OutputManager(outputters)
om.start()

try:
    om.add_report(Report(message="Hello World!"))
    om.add_report(Report(message="Second Message!"))

    counter = 0
    while True:
        time.sleep(1)
        for i in range(0,10):
            counter += 1
            om.add_report(Report(message="counter is at: %s" % counter))
except KeyboardInterrupt:
    print("Stopping...")
finally:
    om.stop()
